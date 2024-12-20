from collections import deque
from pathlib import Path
from typing import NamedTuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)

    def mann(self, other: "Coord") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


DIRS = {
    "^": Coord(0, -1),
    "v": Coord(0, 1),
    "<": Coord(-1, 0),
    ">": Coord(1, 0),
}


class Map:
    def __init__(self, data: str):
        self.walls = set()
        lines = data.split("\n")
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == "#":
                    self.walls.add(Coord(x, y))
                elif c == "S":
                    self.start = Coord(x, y)
                elif c == "E":
                    self.end = Coord(x, y)

    def solve(self) -> tuple[int, list[tuple[Coord, int]]]:
        to_proc = deque([(0, [(self.start, 0)], self.start)])
        seen = {}
        while to_proc:
            cost, locs, loc = to_proc.popleft()
            if seen.get(loc, 999e9) < cost:
                continue
            seen[loc] = cost
            if loc == self.end:
                return cost, locs
            for direct in DIRS.values():
                new_loc = loc + direct
                if new_loc == locs[-1]:
                    continue
                if new_loc not in self.walls:
                    to_proc.append((cost + 1, locs + [(new_loc, cost + 1)], new_loc))

    def solve_cheat(self, best_cost: int, path: list[tuple[Coord, int]]) -> int:
        in_path = dict(path)
        result = 0
        for loc, _cost in path:
            for adj_dir in DIRS:
                cheat1 = loc + DIRS[adj_dir]
                if cheat1 not in self.walls:
                    continue
                cheat2 = cheat1 + DIRS[adj_dir]
                if cheat2 in in_path:
                    score = best_cost - (in_path[cheat2] - in_path[loc]) + 2
                    if best_cost - score >= 100:
                        result += 1
        return result

    @staticmethod
    def solve_cheat_p2(best_cost: int, path: list[tuple[Coord, int]]) -> int:
        in_path = dict(path)
        result = 0
        for loc, _cost in path:
            grid_scan = set()
            for y in range(-20, 21):
                for x in range(abs(y)-20, 21-abs(y)):
                    if (loc.x+x, loc.y+y) in in_path:
                        grid_scan.add(Coord(loc.x+x, loc.y+y))
            for nearby in (l for l in grid_scan if 2 <= loc.mann(l) <= 20):
                score = best_cost - (in_path[nearby] - in_path[loc]) + loc.mann(nearby)
                if best_cost - score >= 100:
                    result += 1
        return result


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    MAP = Map(DATA)
    NO_CHEAT_SCORE, NO_CHEAT_PATH = MAP.solve()

    print(MAP.solve_cheat(NO_CHEAT_SCORE, NO_CHEAT_PATH))
    print(MAP.solve_cheat_p2(NO_CHEAT_SCORE, NO_CHEAT_PATH))
