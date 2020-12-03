import math
from pathlib import Path
from typing import NamedTuple

FILE_DIR = Path(__file__).parent


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)


def read_map(lines):
    tree_pos = set()
    y_max = len(lines)
    x_max = len(lines[0])
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "#":
                tree_pos.add(Coord(x, y))
    return x_max, y_max, tree_pos


def move_check(width, end_y, tree_pos, slope=Coord(3, 1)):
    loc = Coord(0, 0)
    count = 0
    while loc.y <= end_y:
        tree_loc = Coord(loc.x % width, loc.y)
        if tree_loc in tree_pos:
            count += 1
        loc += slope
    return count


def check_all(width, end_y, tree_pos):
    counts = [move_check(width, end_y, tree_pos, Coord(*slope)) for slope in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))]
    return math.prod(counts)


if __name__ == "__main__":
    DATA = (FILE_DIR / "day03.input").read_text().strip()
    repeat_width, end_height, trees = read_map(DATA.split("\n"))
    print(move_check(repeat_width, end_height, trees))
    print(check_all(repeat_width, end_height, trees))
