import heapq
from collections import deque
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

    def solve(self) -> tuple[int, int]:
        to_proc = deque([(0, START_DIR, {self.start}, self.start)])
        best_end_cost = 99e99
        best_seats = set()
        seen = {}
        while to_proc:
            cost, cur_dir, locs, loc = to_proc.popleft()
            if seen.get((loc, cur_dir), 999e9) < cost:
                continue
            seen[(loc, cur_dir)] = cost
            if loc == self.end:
                if cost < best_end_cost:
                    best_seats = set(locs)
                    best_end_cost = cost
                elif best_end_cost == cost:
                    best_end_cost = cost
                else:
                    continue
            forward_loc = loc + DIRS[cur_dir]
            if forward_loc not in self.walls:
                to_proc.appendleft(
                    (cost + 1, cur_dir, locs | {forward_loc}, forward_loc)
                )
            for direct in TURNS[cur_dir]:
                new_loc = loc + DIRS[direct]
                if new_loc not in self.walls:
                    to_proc.append((cost + TURN_COST + 1, direct, locs | {new_loc}, new_loc))
        return best_end_cost, len(best_seats)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    MAP = Map(DATA)

    print("\n".join(str(n) for n in MAP.solve()))
