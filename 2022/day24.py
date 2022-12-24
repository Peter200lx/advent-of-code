import heapq
import math
from pathlib import Path
from typing import List, NamedTuple, Set, Tuple, Dict

INPUT_FILE = Path(__file__).with_suffix(".input")


class Pos(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Pos") -> "Pos":
        if other.x == 0 and other.y == 0:
            return self
        return Pos(self.x + other.x, self.y + other.y)

    def mann(self, other: "Pos") -> int:
        return abs(other.x - self.x) + abs(other.y - self.y)


DIRS = {
    ">": Pos(1, 0),
    "v": Pos(0, 1),
    "<": Pos(-1, 0),
    "^": Pos(0, -1),
}
POSSIBLE = {Pos(0, 0), *DIRS.values()}
START = Pos(0, -1)


def parse(raw_str: str) -> Dict[Pos, Pos]:
    storms: Dict[Pos, Pos] = {}
    for y, line in enumerate(raw_str.split("\n")):
        for x, c in enumerate(line):
            if c in DIRS:
                storms[Pos(x - 1, y - 1)] = DIRS[c]
    return storms


def new_storm(cur: Pos, direc: Pos, x_len: int, y_len: int):
    new_pos = cur + direc
    if 0 <= new_pos.x < x_len and 0 <= new_pos.y < y_len:
        return new_pos
    else:
        if direc == Pos(1, 0):
            return Pos(0, cur.y)
        if direc == Pos(0, 1):
            return Pos(cur.x, 0)
        if direc == Pos(-1, 0):
            return Pos(x_len - 1, cur.y)
        if direc == Pos(0, -1):
            return Pos(cur.x, y_len - 1)


def pre_plot_storms(storms: Dict[Pos, Pos]) -> List[Set[Pos]]:
    x_len = max(p.x for p in storms) + 1
    y_len = max(p.y for p in storms) + 1
    repeat = math.lcm(y_len, x_len)
    storm_tuples = list(storms.items())
    storm_seq = [set(storms)]
    for i in range(1, repeat):
        storm_tuples = [(new_storm(p, d, x_len, y_len), d) for p, d in storm_tuples]
        storm_seq.append({p for p, _d in storm_tuples})
    return storm_seq


def path_find(
    storm_sets: List[Set[Pos]], max_pos: Pos, start: Pos, end: Pos, start_depth: int = 0
) -> int:
    paths: List[Tuple[int, Pos]] = [(start_depth, start)]
    seen: Set[Tuple[int, Pos]] = set()
    while paths:
        depth, cur_loc = heapq.heappop(paths)
        key = depth % len(storm_sets), cur_loc
        if key in seen:
            continue
        seen.add(key)
        new_depth = depth + 1
        for direc in POSSIBLE:
            new_loc = cur_loc + direc
            if new_loc == end:
                return new_depth
            if new_loc in storm_sets[new_depth % len(storm_sets)]:
                continue
            if not (
                new_loc == start
                and cur_loc == start
                or 0 <= new_loc.x <= max_pos.x
                and 0 <= new_loc.y <= max_pos.y
            ):
                continue
            heapq.heappush(paths, (new_depth, new_loc))
    raise NotImplementedError


def solve(storms: Dict[Pos, Pos]) -> int:
    max_pos = Pos(max(p.x for p in storms), max(p.y for p in storms))
    end = Pos(max_pos.x, max_pos.y + 1)
    storm_sets = pre_plot_storms(storms)
    p1_depth = path_find(storm_sets, max_pos, START, end)

    returned_depth = path_find(storm_sets, max_pos, end, START, p1_depth)

    p2_depth = path_find(storm_sets, max_pos, START, end, returned_depth)

    return p1_depth, p2_depth


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().rstrip()
    STORMS = parse(DATA)

    print(solve(STORMS))
