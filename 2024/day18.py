import heapq
from pathlib import Path
from typing import NamedTuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)

    def mann(self, other) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


DIRS = {
    "^": Coord(0, -1),
    "v": Coord(0, 1),
    "<": Coord(-1, 0),
    ">": Coord(1, 0),
}

START = Coord(0, 0)
END = Coord(70, 70)
P1_BYTES = 1024


def printg(walls, path):
    for y in range(END.y + 1):
        print(
            "".join(
                "X" if (x, y) in walls else "O" if (x, y) in path else "."
                for x in range(END.x + 1)
            )
        )


def solve(walls: set[Coord]) -> int:
    to_proc = [(-START.mann(END), 0, {START}, START)]
    square_range = range(0, END.x + 1)
    seen = {}
    while to_proc:
        _mann, cost, locs, loc = heapq.heappop(to_proc)
        if seen.get(loc, 999e9) <= cost:
            continue
        seen[loc] = cost
        if loc == END:
            return cost
        for next_dir in DIRS.values():
            next_loc = loc + next_dir
            if (
                not (next_loc.x in square_range and next_loc.y in square_range)
                or next_loc in walls
            ):
                continue
            if seen.get(next_loc, 99e9) <= cost + 1:
                continue
            heapq.heappush(
                to_proc, (-next_loc.mann(END), cost + 1, locs | {next_loc}, next_loc)
            )
    raise ValueError


def part1(data: str) -> int:
    full_bytes = [
        Coord(int(x), int(y))
        for line in data.split("\n")[:P1_BYTES]
        for x, y in [line.split(",")]
    ]
    return solve(set(full_bytes))


def part2(data: str):
    full_bytes = [
        Coord(int(x), int(y)) for line in data.split("\n") for x, y in [line.split(",")]
    ]
    for i in range(P1_BYTES, len(full_bytes)):
        try:
            solve(set(full_bytes[:i]))
        except ValueError:
            return f"{full_bytes[i-1].x},{full_bytes[i-1].y}"


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    print(part1(DATA))
    print(part2(DATA))
