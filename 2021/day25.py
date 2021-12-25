from typing import Tuple, NamedTuple, Set
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int


def step(
    east_herd: Set[Coord], south_herd: Set[Coord], max_size: Coord
) -> Tuple[Set[Coord], Set[Coord]]:
    all_points = east_herd | south_herd
    east_herd = {
        Coord(*t) if (t := ((c.x + 1) % max_size.x, c.y)) not in all_points else c
        for c in east_herd
    }
    all_points = east_herd | south_herd
    south_herd = {
        Coord(*t) if (t := (c.x, (c.y + 1) % max_size.y)) not in all_points else c
        for c in south_herd
    }
    return east_herd, south_herd


def solve(east_herd: Set[Coord], south_herd: Set[Coord]) -> int:
    maxx = max(max(c.x for c in south_herd), max(c.x for c in east_herd))
    maxy = max(max(c.y for c in south_herd), max(c.y for c in east_herd))
    max_size = Coord(maxx + 1, maxy + 1)
    last_east = last_south = None
    step_count = 0
    while not (last_south == south_herd and last_east == east_herd):
        last_east, last_south = east_herd, south_herd
        east_herd, south_herd = step(east_herd, south_herd, max_size)
        step_count += 1
    return step_count


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    EAST_HERD = {
        Coord(x, y)
        for y, line in enumerate(DATA.split("\n"))
        for x, c in enumerate(line)
        if c == ">"
    }
    SOUTH_HERD = {
        Coord(x, y)
        for y, line in enumerate(DATA.split("\n"))
        for x, c in enumerate(line)
        if c == "v"
    }
    print(solve(EAST_HERD, SOUTH_HERD))
