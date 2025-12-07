from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int


def parse(lines: str):
    start = None
    splitters = []
    for y, line in enumerate(lines.split("\n")):
        for x, c in enumerate(line):
            if c == "S":
                start = Coord(x, y)
            elif c == "^":
                splitters.append(Coord(x, y))
    return start, splitters, y


def part1(start, splitters, end_y) -> int:
    y_level = start.y
    x_spouts = {start.x}
    splits = 0
    while y_level <= end_y:
        y_level += 1
        next_x_spouts = set()
        for x in x_spouts:
            if (x, y_level) in splitters:
                next_x_spouts |= {x - 1, x + 1}
                splits += 1
            else:
                next_x_spouts.add(x)
        x_spouts = next_x_spouts
    return splits


def part2(start, splitters, end_y) -> int:
    y_level = start.y
    x_spouts = {start.x: 1}
    while y_level <= end_y:
        y_level += 1
        next_x_spouts = defaultdict(int)
        for x, to_here in x_spouts.items():
            if (x, y_level) in splitters:
                for new_x in (x - 1, x + 1):
                    next_x_spouts[new_x] += to_here
            else:
                next_x_spouts[x] += to_here
        x_spouts = next_x_spouts
    return sum(x_spouts.values())


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    START, SPLITTERS, END_Y = parse(DATA)

    print(part1(START, SPLITTERS, END_Y))
    print(part2(START, SPLITTERS, END_Y))
