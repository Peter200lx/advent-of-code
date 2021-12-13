from dataclasses import dataclass
from pathlib import Path
from typing import Set

INPUT_FILE = Path(__file__).with_suffix(".input")


@dataclass
class Cave:
    name: str
    adjacent: Set["Cave"]
    large: bool = False

    def __hash__(self):
        return self.name.__hash__()

    def navigate_to_end(self, my_path: Set[str] = None, dupe_cave: bool = True) -> int:
        my_path = my_path or set()
        if not self.large and self.name in my_path:
            if dupe_cave or self.name == "start":
                return 0
            dupe_cave = True
        if self.name == "end":
            return 1

        my_path = my_path | {self.name}
        return sum(cave.navigate_to_end(my_path, dupe_cave) for cave in self.adjacent)


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
    print((STARTING_CAVE.navigate_to_end()))
    print((STARTING_CAVE.navigate_to_end(dupe_cave=False)))
