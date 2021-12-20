from pathlib import Path
from typing import NamedTuple, Dict, Set

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)


def step(grid: Set[Coord], enhance: Dict[int, bool], depth=0):
    new_grid = set()
    minx, maxx = min(p.x for p in grid), max(p.x for p in grid)
    miny, maxy = min(p.y for p in grid), max(p.y for p in grid)
    for cury in range(miny - 1, maxy + 2):
        for curx in range(minx - 1, maxx + 2):
            num = 0
            for delta_y in range(-1, 2):
                for delta_x in range(-1, 2):
                    num <<= 1
                    scan_x, scan_y = curx + delta_x, cury + delta_y
                    if not (
                        minx - 1 < scan_x < maxx + 1 and miny - 1 < scan_y < maxy + 1
                    ):
                        if depth % 2 == 1:
                            if enhance[0]:
                                num |= 1
                        else:
                            if enhance[511]:
                                num |= 1
                    elif (scan_x, scan_y) in grid:
                        num |= 1
            if enhance[num]:
                new_grid.add(Coord(curx, cury))
    return new_grid


def solve(grid: Set[Coord], enhance: Dict[int, bool]):
    for i in range(50):
        grid = step(grid, enhance, depth=i)
        if i == 1:
            print(len(grid))
    print(len(grid))


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    ALGO_STR, START_STR = DATA.split("\n\n")
    ALGORITHM = {i: s == "#" for i, s in enumerate(ALGO_STR)}
    START = {
        Coord(x, y)
        for y, line in enumerate(START_STR.split("\n"))
        for x, s in enumerate(line)
        if s == "#"
    }
    solve(START, ALGORITHM)
