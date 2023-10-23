from __future__ import annotations
from dataclasses import dataclass

from mountain import Mountain
from data_structures.linked_stack import LinkedStack
from typing import TYPE_CHECKING, Union

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality

@dataclass
class TrailSplit:
    """
    A split in the trail.
       ___path_top____
      /               \
    -<                 >-path_follow-
      \__path_bottom__/
    """

    path_top: Trail
    path_bottom: Trail
    path_follow: Trail

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""
        return self.path_follow.store


@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--
    """

    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """Removes the mountain at the beginning of this series."""
        return self.following.store

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain in series before the current one."""
        new_mountain_before = TrailSeries(mountain, Trail(self))
        return new_mountain_before

    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path."""
        new_empty_branch_before = TrailSplit(Trail(None), Trail(None), Trail(self))
        return new_empty_branch_before

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain after the current mountain, but before the following trail."""
        new_mountain_after = TrailSeries(self.mountain, Trail(TrailSeries(mountain, self.following)))
        return new_mountain_after

    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail."""
        new_empty_branch_after = TrailSeries(self.mountain, Trail(TrailSplit(Trail(None), Trail(None), self.following)))
        return new_empty_branch_after


TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """Adds a mountain before everything currently in the trail."""
        new_mountain_before = Trail(TrailSeries(mountain, self))
        return new_mountain_before

    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail."""
        empty_branch_before = Trail(TrailSplit(Trail(None), Trail(None), self))
        return empty_branch_before

    def follow_path(self, personality: WalkerPersonality) -> None:
        """
        Follow a path and add mountains according to a personality.

        Complexity:
        - O(n), where n is the length of path taken by the walker, and it depends on the decisions made by the walker
        - Best case = Worst case
        - The function iterates through each path taken by the walker in the trail exactly once
        - So the run time is directly proportional to the length of path in the trail
        - Time complexity of all operation in the loop is O(1)
        """
        next_path = self.store
        path_follow_tracker = LinkedStack()

        while True:
            if isinstance(next_path, TrailSplit):
                path_follow_tracker.push(next_path.path_follow)
                next_path = next_path.path_top.store if personality.select_branch(next_path.path_top, next_path.path_bottom) else next_path.path_bottom.store

            elif isinstance(next_path, TrailSeries):
                personality.add_mountain(next_path.mountain)
                next_path = next_path.following.store

            elif not next_path and not path_follow_tracker.is_empty():
                next_path = path_follow_tracker.pop().store

            else:
                break

    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        list_of_trails = [self.store]
        list_of_mountains = []
        while list_of_trails:
            current = list_of_trails.pop()
            if isinstance(current, TrailSeries):
                list_of_trails.append(current.following.store)
                list_of_mountains.append(current.mountain)
            elif isinstance(current, TrailSplit):
                list_of_trails.append(current.path_top.store)
                list_of_trails.append(current.path_bottom.store)
                list_of_trails.append(current.path_follow.store)
        return list_of_mountains

    def length_k_paths(self, k) -> list[list[Mountain]]:
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        paths_list = []
        trail_split_list = []
        mountains = []
        self.length_k_paths_aux(self.store, paths_list, trail_split_list, mountains)
        return [path for path in paths_list if len(path) == k]

    def length_k_paths_aux(self, current_path: TrailStore, paths_list: list[list[Mountain]], trail_split_list, current_mountains: list[Mountain]):

        if current_path is None:
            if not trail_split_list:
                paths_list.append(current_mountains)
            else:
                next_path = trail_split_list.pop()
                self.length_k_paths_aux(next_path, paths_list, trail_split_list, current_mountains)

        elif isinstance(current_path, TrailSeries):
            current_mountains.append(current_path.mountain)
            self.length_k_paths_aux(current_path.following.store, paths_list, trail_split_list, current_mountains)

        elif isinstance(current_path, TrailSplit):
            previous_trail_split = trail_split_list[-1] if trail_split_list else None
            trail_split_list.append(current_path.path_follow.store)
            new_top_path_list = current_mountains.copy()
            self.length_k_paths_aux(current_path.path_top.store, paths_list, trail_split_list, new_top_path_list)

            trail_split_list.append(previous_trail_split)
            trail_split_list.append(current_path.path_follow.store)
            new_bottom_path_list = current_mountains.copy()
            self.length_k_paths_aux(current_path.path_bottom.store, paths_list, trail_split_list, new_bottom_path_list)