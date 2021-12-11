from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, NamedTuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)


ADJACENT = [
    Coord(-1, -1),
    Coord(1, 1),
    Coord(-1, 1),
    Coord(1, -1),
    Coord(-1, 0),
    Coord(1, 0),
    Coord(0, 1),
    Coord(0, -1),
]


@dataclass
class Squid:
    coord: Coord
    step: int
    adjacent: List["Squid"]
    flashed: bool = False

    def run(self):
        self.step += 1
        if self.step > 9:
            if self.flashed:
                return
            self.flashed = True
            for other in self.adjacent:
                other.run()

    def reset(self):
        if self.flashed:
            self.step = 0
            self.flashed = False


def build_adjacent(grid: Dict[Coord, "Squid"]):
    for squid in grid.values():
        squid.adjacent = [
            grid[squid.coord + adj] for adj in ADJACENT if squid.coord + adj in grid
        ]


def run_p1(grid: Dict[Coord, "Squid"], steps: int = 100) -> int:
    flashes = 0
    for i in range(steps):
        for squid in grid.values():
            squid.run()
        flashes += sum(squid.flashed for squid in grid.values())
        for squid in grid.values():
            squid.reset()
    return flashes


def run_p2(grid: Dict[Coord, "Squid"], steps_so_far: int = 100) -> int:
    while not all(squid.flashed for squid in grid.values()):
        for squid in grid.values():
            squid.reset()
        for squid in grid.values():
            squid.run()
        steps_so_far += 1
    return steps_so_far


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    GRID = {
        Coord(x, y): Squid(Coord(x, y), int(n), list())
        for y, line in enumerate(DATA.split("\n"))
        for x, n in enumerate(line)
    }
    build_adjacent(GRID)
    print(run_p1(GRID))
    print(run_p2(GRID))
