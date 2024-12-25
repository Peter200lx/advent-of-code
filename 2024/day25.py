from pathlib import Path
from typing import NamedTuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int


def part1(sequences):
    locks = [l for l in sequences if (0, 0) in l]
    keys = [k for k in sequences if (0, 6) in k]
    no_overlaps = 0
    for lock in locks:
        for key in keys:
            if not lock & key:
                no_overlaps += 1
    return no_overlaps


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    SEQUENCES = [
        {
            Coord(x, y)
            for y, line in enumerate(chunk.split("\n"))
            for x, c in enumerate(line)
            if c == "#"
        }
        for chunk in DATA.split("\n\n")
    ]

    print(part1(SEQUENCES))
