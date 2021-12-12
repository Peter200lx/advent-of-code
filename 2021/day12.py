from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Set

INPUT_FILE = Path(__file__).with_suffix(".input")


@dataclass
class Cave:
    name: str
    adjacent: Set["Cave"]
    large: bool = False

    def __hash__(self):
        return self.name.__hash__()

    def __init__(self, name: str):
        self.name = name
        self.adjacent = set()
        if name[0].isupper():
            self.large = True

    def navigate_to_end(
        self, my_path: List[str], list_o_paths: List[List[str]], dupe_cave: str = None
    ) -> List[List[str]]:
        if not self.large and self.name in my_path:
            if self.name == dupe_cave and my_path.count(self.name) == 1:
                pass
            else:
                return list_o_paths
        if self.name == "start":
            from_cave = None
        elif self.name == "end":
            my_path.append(self.name)
            list_o_paths.append(my_path)
            return list_o_paths
        else:
            from_cave = my_path[-1]

        my_path.append(self.name)
        for cave in self.adjacent - {from_cave}:
            cave.navigate_to_end(my_path[:], list_o_paths, dupe_cave)
        return list_o_paths


def build_underground(in_str: str) -> Tuple[Cave, Set[str]]:
    all_caves = {}
    start = None
    for line in in_str.split("\n"):
        first, second = line.split("-")
        for cave in first, second:
            if cave not in all_caves:
                all_caves[cave] = Cave(cave)
                if cave == "start":
                    start = all_caves[cave]
        all_caves[first].adjacent.add(all_caves[second])
        all_caves[second].adjacent.add(all_caves[first])
    small_caves = {
        cave.name
        for cave in all_caves.values()
        if not cave.large and cave.name not in ("start", "end")
    }
    return start, small_caves


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    STARTING_CAVE, SMALL_CAVES = build_underground(DATA)
    print(len(STARTING_CAVE.navigate_to_end([], [])))
    P2_PATHS = [STARTING_CAVE.navigate_to_end([], [], small) for small in SMALL_CAVES]
    print(len({"->".join(path) for path_attempt in P2_PATHS for path in path_attempt}))
