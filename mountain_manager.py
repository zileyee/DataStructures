from mountain import Mountain
from double_key_table import DoubleKeyTable
from algorithms.mergesort import *
from typing import List

class MountainManager:

    def __init__(self) -> None:
        """
        Complexity:
        -O(1) since we assumed that all Double Key Table methods are O(1).
        -Best case = Worst case
        """
        self.manager = DoubleKeyTable()

    def add_mountain(self, mountain: Mountain):
        """
        Complexity:
        -O(1) since we assumed that all Double Key Table methods are O(1).
        -Best case = Worst case
        """
        self.manager[str(mountain.difficulty_level), mountain.name] = mountain

    def remove_mountain(self, mountain: Mountain):
        """
        Complexity:
        -O(1) since we assumed that all Double Key Table methods are O(1).
        -Best case = Worst case
        """
        del self.manager[str(mountain.difficulty_level), mountain.name]

    def edit_mountain(self, old: Mountain, new: Mountain):
        """
        Complexity:
        -O(1) since we assumed that all Double Key Table methods are O(1).
        -Best case = Worst case
        """
        del self.manager[str(old.difficulty_level), old.name]
        self.manager[str(new.difficulty_level), new.name] = new
        
    def mountains_with_difficulty(self, diff: int) -> List[Mountain]:
        """
        Return a list of all mountains with this difficulty.

        Complexity:
        -O(1) since we assumed that all Double Key Table methods are O(1).
        -Best case = Worst case
        """
        return self.manager.values(str(diff))

    def group_by_difficulty(self):
        """
        Complexity:
        -Best case: O(1) if there is only one mountain to sort.
        -Worst case: O(N*logN) when there are N mountains to sort.
        """
        mountain_list = self.manager.keys()
        sorted_mountain_list = mergesort(mountain_list)
        return [self.manager.values(mountain) for mountain in sorted_mountain_list]

