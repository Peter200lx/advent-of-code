import heapq
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


ADJACENT = [Coord(-1, 0), Coord(0, -1), Coord(0, 1), Coord(1, 0)]


@dataclass
class Cave:
    risk: int
    coord: Coord
    adjacent: List["Cave"]

    def __lt__(self, other):
        return self.risk < other.risk

    def find_paths_from_start(self, finish: Coord):
        heap = []
        heapq.heappush(heap, (0, self))
        coord_cost = {}
        while heap:
            risk_so_far, cave = heapq.heappop(heap)
            if coord_cost.get(cave.coord, 999999999) <= risk_so_far:
                continue
            if cave.coord == finish:
                return risk_so_far
            coord_cost[cave.coord] = risk_so_far
            for other_cave in cave.adjacent:
                other_risk = risk_so_far + other_cave.risk
                if coord_cost.get(other_cave.coord, 999999999) <= other_risk:
                    continue
                heapq.heappush(heap, (other_risk, other_cave))


def build_adjacent(grid: Dict[Coord, Cave]) -> Tuple[Cave, Coord]:
    start = None
    maxx = max(cave.coord.x for cave in grid.values())
    maxy = max(cave.coord.y for cave in grid.values())
    for cave in grid.values():
        if cave.coord == (0, 0):
            start = cave
        cave.adjacent = [
            grid[cave.coord + adj] for adj in ADJACENT if cave.coord + adj in grid
        ]
    return start, Coord(maxx, maxy)


def quintuple_grid(grid: Dict[Coord, Cave]):
    maxx = max(cave.coord.x for cave in grid.values()) + 1
    maxy = max(cave.coord.y for cave in grid.values()) + 1
    for y in range(maxy * 5):
        for x in range(maxx * 5):
            if (x, y) in grid:
                continue
            if x < maxx:
                cost = grid[Coord(x, y - (maxy))].risk + 1
            else:
                cost = grid[Coord(x - (maxx), y)].risk + 1
            grid[Coord(x, y)] = Cave(cost if cost <= 9 else 1, Coord(x, y), list())


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    GRID = {
        Coord(x, y): Cave(int(n), Coord(x, y), list())
        for y, line in enumerate(DATA.split("\n"))
        for x, n in enumerate(line)
    }
    START, END_COORD = build_adjacent(GRID)
    print(START.find_paths_from_start(finish=END_COORD))
    quintuple_grid(GRID)
    START, END_COORD = build_adjacent(GRID)
    print(START.find_paths_from_start(finish=END_COORD))
