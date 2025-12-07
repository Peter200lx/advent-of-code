from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int


def parse(lines: str) -> tuple[Coord, list[Coord], int]:
    start = None
    splitters = []
    for y, line in enumerate(lines.split("\n")):
        for x, c in enumerate(line):
            if c == "S":
                start = Coord(x, y)
            elif c == "^":
                splitters.append(Coord(x, y))
    return start, splitters, y


def solve(start: Coord, splitters: list[Coord], end_y: int) -> tuple[int, int]:
    y_level = start.y
    x_spouts = {start.x: 1}
    splits = 0
    while y_level <= end_y:
        y_level += 1
        next_x_spouts = defaultdict(int)
        for x, to_here in x_spouts.items():
            if (x, y_level) in splitters:
                splits += 1
                for new_x in (x - 1, x + 1):
                    next_x_spouts[new_x] += to_here
            else:
                next_x_spouts[x] += to_here
        x_spouts = next_x_spouts
    return splits, sum(x_spouts.values())


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    START, SPLITTERS, END_Y = parse(DATA)

    print("\n".join(str(n) for n in solve(START, SPLITTERS, END_Y)))
