import heapq
from pathlib import Path
from typing import NamedTuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)

    def add_int(self, val):
        return Coord(self.x + val, self.y + val)


DIRS = {
    "^": Coord(0, -1),
    "v": Coord(0, 1),
    "<": Coord(-1, 0),
    ">": Coord(1, 0),
}
TURNS = {
    "^": "<>",
    "v": "<>",
    "<": "^v",
    ">": "^v",
}

START_DIR = ">"
TURN_COST = 1000


class Map:
    def __init__(self, data: str):
        self.walls = set()
        self.bot = None
        for y, line in enumerate(data.split("\n")):
            for x, c in enumerate(line):
                if c == "#":
                    self.walls.add(Coord(x, y))
                elif c == "S":
                    self.start = Coord(x, y)
                elif c == "E":
                    self.end = Coord(x, y)

    def p1(self) -> int:
        to_proc = [(0, START_DIR, self.start)]
        seen = {}
        while to_proc:
            cost, cur_dir, loc = heapq.heappop(to_proc)
            if loc == self.end:
                return cost
            if seen.get((loc, cur_dir), 999e9) < cost:
                continue
            seen[(loc, cur_dir)] = cost
            forward_loc = loc + DIRS[cur_dir]
            if forward_loc not in self.walls:
                heapq.heappush(to_proc, (cost + 1, cur_dir, forward_loc))
            for direct in TURNS[cur_dir]:
                heapq.heappush(to_proc, (cost + TURN_COST, direct, loc))

    def p2(self) -> int:
        to_proc = [(0, START_DIR, {self.start}, self.start)]
        best_end_cost = 99e99
        best_seats = set()
        seen = {}
        while to_proc:
            cost, cur_dir, locs, loc = heapq.heappop(to_proc)
            if loc == self.end:
                best_end_cost = cost
                best_seats |= locs
            if cost > best_end_cost:
                return len(best_seats)
            if seen.get((loc, cur_dir), 999e9) < cost:
                continue
            seen[(loc, cur_dir)] = cost
            forward_loc = loc + DIRS[cur_dir]
            if forward_loc not in self.walls:
                heapq.heappush(
                    to_proc, (cost + 1, cur_dir, locs | {forward_loc}, forward_loc)
                )
            for direct in TURNS[cur_dir]:
                heapq.heappush(to_proc, (cost + TURN_COST, direct, locs, loc))


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    MAP = Map(DATA)

    print(MAP.p1())
    print(MAP.p2())
