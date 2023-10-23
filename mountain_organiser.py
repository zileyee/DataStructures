from __future__ import annotations
from algorithms.mergesort import *
from algorithms.binary_search import *
from mountain import Mountain

class MountainOrganiser:

    def __init__(self) -> None:
        """
        Complexity:
        -O(1) to initialize a list
        -Best case = Worst case
        """
        self.list_of_mountains = []

    def cur_position(self, mountain: Mountain) -> int:
        """
        Implement binary search to find the index of the given mountain in the sorted list of mountains.

        Complexity:
        -Best case: O(1) when the mountain you are trying to search for is in the middle of the sorted list of mountains.
        -Worst case: O(logN) when the mountain you are trying to search for is at the front or end of the sorted list of mountains.
        -N is len(self.list_of_mountains).
        """
        lo = 0
        hi = len(self.list_of_mountains) - 1

        while lo <= hi:
            mid = (lo + hi) // 2
            search_mountain = self.list_of_mountains[mid]

            if search_mountain.length == mountain.length:
                if search_mountain.name == mountain.name:
                    return mid
                elif search_mountain.name < mountain.name:
                    lo = mid + 1
                else:
                    hi = mid - 1
            elif search_mountain.length < mountain.length:
                lo = mid + 1
            else:
                hi = mid - 1

        raise KeyError

    def add_mountains(self, mountains: list[Mountain]) -> None:
        """
        binary search to find the correct position for each mountain in the sorted list, and then inserts the mountain into the list at that position.

        Complexity:
        -Best case: O(N) where N is len(mountains) and every mountain is inserted into the middle of the list.
        -Thus, the while loop only iterate once for every mountain.
        -Worst case: O(N*logM) where N is len(mountains) and M is len(self.list_of_mountains).
        -Every mountain is inserted at the front or end of the list.
        -Thus, the binary search while loop will iterate logM times.
        """
        for mountain in mountains:  # O(N)
            left, right = 0, len(self.list_of_mountains) - 1
            index = None

            while left <= right:  # O(logM)
                mid = (left + right) // 2
                search_mountain = self.list_of_mountains[mid]
                if search_mountain.length < mountain.length:
                    left = mid + 1
                elif search_mountain.length > mountain.length:
                    right = mid - 1
                elif search_mountain.name < mountain.name:
                    left = mid + 1
                elif search_mountain.name > mountain.name:
                    right = mid - 1
                else:
                    index = mid
                    break

            if index is None:
                index = left

            self.list_of_mountains.insert(index, mountain)