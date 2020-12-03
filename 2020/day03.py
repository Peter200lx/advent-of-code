import math
from pathlib import Path
from typing import NamedTuple, Set

FILE_DIR = Path(__file__).parent


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)


class Map(NamedTuple):
    width: int
    height: int
    trees: Set[Coord]

    @staticmethod
    def read_lines(lines):
        height = len(lines)
        width = len(lines[0])
        trees: Set[Coord] = set()
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == "#":
                    trees.add(Coord(x, y))
        return Map(width, height, trees)


def move_check(forest: Map, slope: Coord = Coord(3, 1)):
    loc = Coord(0, 0)
    count = 0
    while loc.y <= forest.height:
        tree_loc = Coord(loc.x % forest.width, loc.y)
        if tree_loc in forest.trees:
            count += 1
        loc += slope
    return count


def check_all(forest: Map):
    all_angles = [Coord(*angle) for angle in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))]
    return math.prod(move_check(forest, slope) for slope in all_angles)


if __name__ == "__main__":
    DATA = (FILE_DIR / "day03.input").read_text().strip()
    FOREST = Map.read_lines(DATA.split("\n"))
    print(move_check(FOREST))
    print(check_all(FOREST))
