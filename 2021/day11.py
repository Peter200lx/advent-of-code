from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, NamedTuple, Tuple

INPUT_FILE = Path(__file__).with_suffix(".input")

P1_STEP_COUNT = 100


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)


# fmt: off
ADJACENT = [
    Coord(-1, -1), Coord(-1, 0), Coord(-1, 1),
    Coord(0, -1),                Coord(0, 1),
    Coord(1, -1),  Coord(1, 0),  Coord(1, 1),
]
# fmt: on


@dataclass
class Squid:
    coord: Coord
    step: int
    adjacent: List["Squid"]
    flashed: bool = False

    def run(self):
        self.step += 1
        if not self.flashed and self.step > 9:
            self.flashed = True
            [other.run() for other in self.adjacent]

    def reset(self):
        if self.flashed:
            self.step = 0
            self.flashed = False


def build_adjacent(grid: Dict[Coord, Squid]):
    for squid in grid.values():
        squid.adjacent = [
            grid[squid.coord + adj] for adj in ADJACENT if squid.coord + adj in grid
        ]


def run(grid: List[Squid]) -> Tuple[int, int]:
    flashes = 0
    for i in range(1, 9999999):
        [squid.reset() for squid in grid]
        [squid.run() for squid in grid]
        if i <= P1_STEP_COUNT:
            flashes += sum(squid.flashed for squid in grid)
        elif all(squid.flashed for squid in grid):
            return flashes, i


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    GRID = {
        Coord(x, y): Squid(Coord(x, y), int(n), list())
        for y, line in enumerate(DATA.split("\n"))
        for x, n in enumerate(line)
    }
    build_adjacent(GRID)
    print(run(list(GRID.values())))
