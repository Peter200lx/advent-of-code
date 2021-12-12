from dataclasses import dataclass
from pathlib import Path
from typing import List, Set

INPUT_FILE = Path(__file__).with_suffix(".input")


@dataclass
class Cave:
    name: str
    adjacent: Set["Cave"]
    large: bool = False

    def __hash__(self):
        return self.name.__hash__()

    def navigate_to_end(
        self, my_path: List[str] = None, list_o_paths: List[List[str]] = None, dupe_cave: bool = None
    ) -> List[List[str]]:
        my_path = my_path or []
        list_o_paths = list_o_paths if list_o_paths is not None else []
        if not self.large and self.name in my_path:
            if dupe_cave is None or dupe_cave or self.name in {"start", "end"}:
                return list_o_paths
            dupe_cave = True
        my_path.append(self.name)
        if self.name == "end":
            list_o_paths.append(my_path)
            return list_o_paths

        from_cave = my_path[-1] if my_path else None
        for cave in self.adjacent - {from_cave}:
            cave.navigate_to_end(my_path[:], list_o_paths, dupe_cave)
        return list_o_paths


def build_underground(in_str: str) -> Cave:
    all_caves = {}
    start = None
    for line in in_str.split("\n"):
        first, second = line.split("-")
        for cave in first, second:
            if cave not in all_caves:
                all_caves[cave] = Cave(cave, set(), cave.isupper())
                if cave == "start":
                    start = all_caves[cave]
        all_caves[first].adjacent.add(all_caves[second])
        all_caves[second].adjacent.add(all_caves[first])
    return start


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    STARTING_CAVE = build_underground(DATA)
    print(len(STARTING_CAVE.navigate_to_end()))
    print(len(STARTING_CAVE.navigate_to_end(dupe_cave=False)))
