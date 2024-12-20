from collections import deque, Counter
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
TURNS = {
    "^": "<>",
    "v": "<>",
    "<": "^v",
    ">": "^v",
}

START_DIR = ">"


class Map:
    def __init__(self, data: str):
        self.walls = set()
        self.bot = None
        lines = data.split("\n")
        self.max = Coord(len(lines[0]), len(lines))
        self.in_play_x = range(1, self.max.x - 2)
        self.in_play_y = range(1, self.max.y - 2)
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == "#":
                    self.walls.add(Coord(x, y))
                elif c == "S":
                    self.start = Coord(x, y)
                elif c == "E":
                    self.end = Coord(x, y)

    def solve(self) -> tuple[int, list[tuple[Coord, int]]]:
        to_proc = deque([(0, START_DIR, [(self.start, 0)], self.start)])
        seen = {}
        while to_proc:
            cost, cur_dir, locs, loc = to_proc.popleft()
            if seen.get((loc, cur_dir), 999e9) < cost:
                continue
            seen[(loc, cur_dir)] = cost
            if loc == self.end:
                return cost, locs
            for direct in TURNS[cur_dir] + cur_dir:
                new_loc = loc + DIRS[direct]
                if new_loc not in self.walls:
                    to_proc.append(
                        (cost + 1, direct, locs + [(new_loc, cost + 1)], new_loc)
                    )

    def solve_cheat(self, best_cost: int, path: list[tuple[Coord, int]]) -> int:
        in_path = dict(path)
        seen_cheats = {}
        result = 0
        for i, (loc, _) in enumerate(path):
            if not loc:
                continue
            for adj_dir in DIRS:
                cheat1 = loc + DIRS[adj_dir]
                if cheat1 not in self.walls:
                    continue
                key = cheat1
                if key in seen_cheats:
                    continue
                cheat2 = cheat1 + DIRS[adj_dir]
                if cheat2 in in_path:
                    # self.walls.remove(cheat1)
                    score = best_cost - (in_path[cheat2] - in_path[loc]) + 2
                    # score, _path = self.solve()
                    seen_cheats[key] = best_cost - score
                    # self.walls.add(cheat1)
                    if best_cost - score >= 100:
                        result += 1
        # print(Counter(v for v in seen_cheats.values() if v ))
        return result

    def solve_cheat_p2(self, best_cost: int, path: list[tuple[Coord, int]]) -> int:
        in_path = dict(path)
        seen_cheats = {}
        result = 0
        for i, (loc, _) in enumerate(path):
            if not loc:
                continue
            for nearby in (l for l in in_path if 2 <= loc.mann(l) <= 20):
                if nearby == loc:
                    continue
                key = (loc, nearby)
                score = best_cost - (in_path[nearby] - in_path[loc]) + loc.mann(nearby)
                seen_cheats[key] = best_cost - score
                if best_cost - score >= 100:
                    result += 1
        # print(Counter(v for v in seen_cheats.values() if v ))
        return result


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    MAP = Map(DATA)
    NO_CHEAT_SCORE, NO_CHEAT_PATH = MAP.solve()

    print(MAP.solve_cheat(NO_CHEAT_SCORE, NO_CHEAT_PATH))
    print(MAP.solve_cheat_p2(NO_CHEAT_SCORE, NO_CHEAT_PATH))
