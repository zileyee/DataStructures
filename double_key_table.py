from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')


class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise hash1 should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise hash2 should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241,
                   786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes: list | None = None, internal_sizes: list | None = None) -> None:
        """
        Initialize the DoubleKeyTable.

        Complexity:
        -O(n) where n is the size of the array stored in top_level_hash_table
        -Best case = Worst case
        """
        if sizes:
            self.TABLE_SIZES = sizes

        self.internal_table_sizes = internal_sizes
        self.size_index = 0
        self.top_level_hash_table = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """
        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % len(self.top_level_hash_table.array)
            a = a * self.HASH_BASE % (len(self.top_level_hash_table.array) - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """
        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.

        Complexity:
        -Best case: O(hash1(key1) + __init()__ + hash2(key2)) when the first position is empty.
                    __init()__ is the method from LinearProbeTable class.
        -Worst case: O(hash1(key) + N*(Comp== + _linear_probe())) when we've searched the entire table
                     N is the table_size
                     _linear_probe() is the method from LinearProbeTable class
        """
        position1 = self.hash1(key1)  # O(hash1)

        for _ in range(self.table_size):  # O(N)

            if self.top_level_hash_table[position1] is None:

                if is_insert:
                    internal_table = LinearProbeTable(self.internal_table_sizes)  # O(__init()__) in LinearProbeTable
                    internal_table.hash = lambda k: self.hash2(k, internal_table)
                    self.top_level_hash_table[position1] = (key1, internal_table)
                    self.count += 1
                    position2 = self.hash2(key2, internal_table)  # O(hash2)
                    return position1, position2

                else:
                    raise KeyError((key1, key2))

            elif self.top_level_hash_table[position1][0] == key1:  # O(Comp==)
                position2 = self.top_level_hash_table[position1][1]._linear_probe(key2, is_insert)  # O(_linear_probe) in hash_table
                return position1, position2

            else:
                position1 = (position1 + 1) % self.table_size

        if is_insert:
            raise FullError("Table is full")
        else:
            raise KeyError((key1, key2))

    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.

        Complexity:
        -O(keys() + yield) as the function only returns a generator object.
        -keys() is the method in this class
        -Best case = Worst case
        """
        for i in range(len(self.keys(key))):  # O(keys())
            yield self.keys(key)[i]  # O(yield)

    def keys(self, key: K1 | None = None) -> list[K1 | K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        Complexity:
        -Best case: O(N) when the key parameter passed in is None and N is table_size.
        -Worst case: O(N*Comp==) when the key we're trying to search for is at the end of the table and N is table_size.
        """
        keys = []
        if key is None:
            for item in self.top_level_hash_table:  # O(N)
                if item:
                    keys.append(item[0])
            return keys

        for i in range(self.table_size):  # O(N)
            if self.top_level_hash_table[i] is not None:
                if self.top_level_hash_table[i][0] == key:  # O(Comp==)
                    return self.top_level_hash_table[i][1].keys()  # O(N)

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.

        Complexity:
        -O(values(key) + yield) as the function only return a generator object.
        -values(key) is the function from this class.
        -Best case = Worst case
        """
        for i in range(len(self.values(key))):
            yield self.values(key)[i]

    def values(self, key: K1 | None = None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.

        Complexity:
        -Best case: O(N*Comp==) when the key is not None and N is the number of elements in the table.
        -Comp== is the time complexity of comparing the key.
        -Worst case: O(N*(M + values())) when the key is None and N is the number of elements in the table.
        -M is the length of list returned by values().
        -values() is the method from LinearProbeTable class.

        """
        res = []
        if key is None:
            for i in range(len(self.top_level_hash_table)):  # O(N)
                pos1 = self.top_level_hash_table[i]
                if pos1 is not None:
                    res.extend(pos1[1].values())  # O(M + values())

        else:
            for i in range(len(self.top_level_hash_table)):  # O(N)
                pos1 = self.top_level_hash_table[i]
                if pos1 is not None and pos1[0] == key:  # O(Comp==)
                    res = pos1[1].values()

        return res

    def __contains__(self, key: tuple[K1, K2]) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        Complexity:
        -O(__getitem()__) where __getitem()__ is the method in this class
        -Best case = Worst case
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.

        Complexity:
        -O(linear_probe()) where linear_probe() is the method from this class.
        -Best case = Worst case
        """
        key1, key2 = key
        position1, position2 = self._linear_probe(key1, key2, False)
        return self.top_level_hash_table[position1][1][key2]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        Complexity:
        -Best case: O(linear probe()) when rehash is not needed.
        -Worst case: O(linear probe() + rehash()) when the load factor exceed 0.5 and a rehash is needed.
        -linear_probe() is the method from this class
        -rehash() is also the method from this class
        """
        key1, key2 = key
        pos1, pos2 = self._linear_probe(key1, key2, True)

        self.top_level_hash_table[pos1][1][key2] = data

        if len(self) > self.table_size / 2:
            self._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.

        Complexity:
        -O(__contains()__ + linear_probe() + __delitem())
        -Best case = Worst case
        -__contains()__ and linear_probe() are both methods in this class.
        -__delitem()_ is the method from LinearProbeTable class.
        """
        if key in self:
            key1, key2 = key
            pos1, pos2 = self._linear_probe(key1, key2, False)
            internal_table = self.top_level_hash_table[pos1][1]
            del internal_table[key2]
            if internal_table.is_empty():
                self.top_level_hash_table[pos1] = None
                self.count -= 1

        else:
            raise KeyError(key)

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        Complexity:
        -Best case: O(1) when size index is equal to len(TABLE_SIZES) and it cannot be resized further.
        -Worst case: O(N + M*(hash1(key1) + __setitem()__)) where N is the size of the new array.
        -M is the number of elements in the old array.
        -hash1(key1) and __setitem()__ both are methods from this class.
        """
        old_array = self.top_level_hash_table
        self.size_index += 1
        if self.size_index == len(self.TABLE_SIZES):
            # Cannot be resized further.
            return
        self.top_level_hash_table = ArrayR(self.TABLE_SIZES[self.size_index])  # O(N)
        self.count = 0
        for item in old_array:  # O(M)
            if item is not None:
                key1, internal_table = item
                pos1 = self.hash1(key1)  # O(hash1(key1))
                self.top_level_hash_table[pos1] = (key1, internal_table)  # O(__setitem()__)

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)

        Complexity:
        -O(1)
        -Best case = Worst case
        """
        return self.TABLE_SIZES[self.size_index]

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table

        Complexity:
        -O(1)
        -Best case = Worst case
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.

        Complexity:
        -O(N*M) where N is the number of elements in the upper table and M is the number of elements in the internal tables.
        -Best case = Worst case
        """
        ret = ""
        for i in range(self.table_size):
            if self.top_level_hash_table[i] is not None:
                for item in self.top_level_hash_table[i][1].array:
                    if item is not None:
                        (key, value) = item
                        ret += "(" + str(self.top_level_hash_table[i][0]) + ", " + str(key) + ", " + str(
                            value) + ")\n"

        return ret
