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


def print_storms(storms: Set[Pos]):
    min_x, max_x = min(p.x for p in storms), max(p.x for p in storms)
    min_y, max_y = min(p.y for p in storms), max(p.y for p in storms)
    print(f"{min_x=} {max_x=}  {min_y=} {max_y=}")
    for y in range(min_y, max_y + 1):
        print(
            "".join(
                "@" if Pos(x, y) in storms else "." for x in range(min_x, max_x + 1)
            )
        )
    print("")


def part_1(storms: Dict[Pos, Pos]) -> int:
    x_max = max(p.x for p in storms)
    y_max = max(p.y for p in storms)
    end = Pos(x_max, y_max + 1)
    storm_sets = pre_plot_storms(storms)
    paths: List[Tuple[int, Pos, List[Pos]]] = [(0, START, [START])]
    seen: Set[Tuple[int, Pos]] = set()
    while paths:
        depth, cur_loc, so_far = heapq.heappop(paths)
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
                new_loc == START
                and cur_loc == START
                or 0 <= new_loc.x <= x_max
                and 0 <= new_loc.y <= y_max
            ):
                continue
            heapq.heappush(paths, (new_depth, new_loc, so_far + [new_loc]))
    raise NotImplementedError


def part_2(storms: Dict[Pos, Pos]) -> int:
    x_max = max(p.x for p in storms)
    y_max = max(p.y for p in storms)
    end = Pos(x_max, y_max + 1)
    storm_sets = pre_plot_storms(storms)
    paths: List[Tuple[int, Pos, List[Pos]]] = [(0, START, [START])]
    seen: Set[Tuple[int, Pos]] = set()
    p1_depth = None
    while paths:
        depth, cur_loc, so_far = heapq.heappop(paths)
        key = depth % len(storm_sets), cur_loc
        if key in seen:
            continue
        seen.add(key)
        new_depth = depth + 1
        for direc in POSSIBLE:
            new_loc = cur_loc + direc
            if new_loc == end:
                p1_depth = new_depth
                paths = []
                break
            if new_loc in storm_sets[new_depth % len(storm_sets)]:
                continue
            if not (
                new_loc == START
                and cur_loc == START
                or 0 <= new_loc.x <= x_max
                and 0 <= new_loc.y <= y_max
            ):
                continue
            heapq.heappush(paths, (new_depth, new_loc, so_far + [new_loc]))

    returned_depth = None
    paths: List[Tuple[int, Pos, List[Pos]]] = [(p1_depth, end, [end])]
    seen: Set[Tuple[int, Pos]] = set()
    while paths:
        depth, cur_loc, so_far = heapq.heappop(paths)
        key = depth % len(storm_sets), cur_loc
        if key in seen:
            continue
        seen.add(key)
        new_depth = depth + 1
        for direc in POSSIBLE:
            new_loc = cur_loc + direc
            if new_loc == START:
                returned_depth = new_depth
                paths = []
                break
            if new_loc in storm_sets[new_depth % len(storm_sets)]:
                continue
            if not (
                new_loc == end
                and cur_loc == end
                or 0 <= new_loc.x <= x_max
                and 0 <= new_loc.y <= y_max
            ):
                continue
            heapq.heappush(paths, (new_depth, new_loc, so_far + [new_loc]))

    paths: List[Tuple[int, Pos, List[Pos]]] = [(returned_depth, START, [START])]
    seen: Set[Tuple[int, Pos]] = set()
    while paths:
        depth, cur_loc, so_far = heapq.heappop(paths)
        key = depth % len(storm_sets), cur_loc
        if key in seen:
            continue
        seen.add(key)
        new_depth = depth + 1
        for direc in POSSIBLE:
            new_loc = cur_loc + direc
            if new_loc == end:
                return p1_depth, new_depth
            if new_loc in storm_sets[new_depth % len(storm_sets)]:
                continue
            if not (
                new_loc == START
                and cur_loc == START
                or 0 <= new_loc.x <= x_max
                and 0 <= new_loc.y <= y_max
            ):
                continue
            heapq.heappush(paths, (new_depth, new_loc, so_far + [new_loc]))


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().rstrip()
    STORMS = parse(DATA)

    print(part_2(STORMS))
