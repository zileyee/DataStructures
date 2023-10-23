from __future__ import annotations
from typing import Generic, TypeVar, List
from data_structures.hash_table import LinearProbeTable

K = TypeVar("K")
V = TypeVar("V")


class InfiniteHashTable(Generic[K, V]):

    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self) -> None:
        """
        Complexity:
        -O(1) as the TABLE_SIZE is a constant value and the run time does not depend on any size of input.
        -Best case = Worst case
        """
        self.table = LinearProbeTable([self.TABLE_SIZE])
        self.level = 0
        self.count = 0
        self.parent_table = None

    def hash(self, key: K) -> int:
        """
        Complexity:
        -O(1)
        -Best case = Worst case
        """
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.

        Complexity:
        -Best case: O(hash(key)) where hash() is the method from this class, it happens when the key is at depth 0 of the table.
        -Worst case: O(get_location() + N*Comp==）when the key is at the deepest level of the table.
        -get_location() is the method from this class.
        -N is the number of levels of table we have to traverse through
        -Comp== is the complexity of comparison of the key.
        """
        position = self.hash(key)

        for _ in range(len(self.table)):
            if self.table[position] == self.MARKER or self.table[position] is None:
                raise KeyError(key)
            if self.table[position][0] == key:
                return self.table[position][1]

        pos = self.hash(key)
        temp = self
        while temp.table.array[pos] is not None:
            current_pos = temp.table.array[pos]
            if current_pos[0] is key:
                return current_pos[1]
            pos = current_pos[1].hash(key)
            temp = current_pos[1]

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        Complexity:
        -Best case: O(hash(key)) when the position at depth 0 is None.
        -hash(key) is the method from this class.
        -Worst case: O(N*(hash + isinstance + Comp==) when we traverse to the deepest level and create a new table.
        -Comp== is the complexity of comparison.
        -N is the number of levels of table we have to traverse through.
        """
        pos = self.hash(key)
        self.count += 1
        if self.table.array[pos] is None:
            self.table.array[pos] = key, value
            return
        temp = self
        level = 0
        while temp is not None:
            pos = temp.hash(self.key_recursion(level, key))
            current_pos = temp.table.array[pos]
            if current_pos is not None:
                if current_pos[0] is not key and not isinstance(current_pos[1], InfiniteHashTable):
                    next_level = InfiniteHashTable()
                    temp.table.array[pos] = self.key_recursion(level, key), next_level
                    level += 1
                    next_level.level = level
                    new_pos = next_level.hash(self.key_recursion(level, current_pos[0]))
                    my_pos = next_level.hash(key)
                    if new_pos != my_pos:
                        temp.table.array[pos][1].table.array[new_pos] = current_pos
                        temp.table.array[pos][1].table.array[my_pos] = key, value
                        return
                    pos_now = next_level.hash(key)
                    temp.table.array[pos][1].table.array[pos_now] = current_pos[0], next_level
                    temp = temp.table.array[pos][1].table.array[pos_now][1]
                    temp.table.array[pos_now] = current_pos
                elif type(current_pos[1]) is InfiniteHashTable:
                    level += 1
                    temp = current_pos[1]
                else:
                    break
            else:
                break

    def key_recursion(self, level, key):
        ret = ""
        for i in range(level + 1):
            if i < len(key):
                ret += key[i]
            else:
                break
        return ret

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

         Remove a key/value pair. If this pair removed leaves only a single pair within the current table,
         then the current table should be collapsed to a single entry in the parent table (This should
         continue upwards until there is a table with multiple pairs or we are at the top table)

        :raises KeyError: when the key doesn't exist.

        Complexity:
        -Best case: O(get_location(key)) when the key is at depth 0.
        -get_location(key) is the method from this class.
        -Worst case: O(get_location(key) + N*(M + isinstance) when deleting the item, the table only have one item left.
        -N is the total depth of the tables.
        -M is the number of elements in the current table.
        """
        temp = self
        self.count -= 1
        loc = self.get_location(key)
        for i in range(len(loc)):
            current_pos = temp.table.array[loc[i]]
            if current_pos is not None:
                if current_pos[0] is key:
                    temp.table.array[loc[i]] = None
                    break
                temp, temp.parent_table = current_pos[1], temp
            else:
                break
        if temp is not None and len(temp.table.keys()) == 1:
            single = self.get_location(temp.table.keys()[0])
            if isinstance(temp.table.values()[0], int):
                for i in range(len(single)-1, 0, -1):
                    if len(temp.table.keys()) == 1 and temp.parent_table is not None:
                        temp.parent_table.table.array[single[i-1]] = temp.table.array[single[i]]
                        temp = temp.parent_table

    def __len__(self):
        """
        Complexity:
        -O(1) since returning the value of an instance variable is constant.
        -Best case = Worst case
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.
        Not required but may be a good testing tool.
        """
        pass

    def get_location(self, key) -> List[int]:
        """
        Get the sequence of positions required to access this key.
        Returns a list containing the indices required to retrieve a key. For example, get_location(linger) == [4, 1, 6, 25]

        :raises KeyError: when the key doesn't exist.

        Complexity:
        -Best case: O(hash(key)), when the key is at depth 0.
        -hash(key) is the method from this class.
        -Worst case: O(n), where k is the length of the sequence required to access the key.
        -The function traverses the linked list at each level only until it finds the key or reaches the end of the list.
        """
        pos = self.hash(key)
        sequence_of_pos = [pos]
        infinite_table = self.table
        if infinite_table is not None:
            current_pos = infinite_table.array[pos]
            while current_pos is not None:
                if type(current_pos[1]) is int and current_pos[0] is not key:
                    raise KeyError
                elif current_pos[0] is key:
                    break
                pos = current_pos[1].hash(key)
                sequence_of_pos.append(pos)
                infinite_table = current_pos[1].table
                current_pos = infinite_table.array[pos]
            return sequence_of_pos
        raise KeyError

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

