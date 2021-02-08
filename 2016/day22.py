import heapq
import re
from itertools import permutations
from pathlib import Path
from typing import List, Dict, Tuple, Iterable, Optional

FILE_DIR = Path(__file__).parent

PARSE_RE = re.compile(r".dev.grid.node-x(?P<x>\d+)-y(?P<y>\d+)\s+(?P<size>\d+)T\s+(?P<used>\d+)T\s+(?P<avail>\d+)T.*")

Point = Tuple[int, int]


class Machine:
    def __init__(self, my_id: Point, size: str, used: str, avail: str):
        self.id = my_id
        self.size = int(size)
        self.used = int(used)
        self.avail = int(avail)
        self.goal = False

    def __repr__(self):
        return f"Machine({str(self.id):>8}: s{self.size}, u{self.used}, a{self.avail})"

    def is_block(self):
        return self.size > 100

    def is_empty(self):
        return self.used == 0

    def grid_chr(self) -> str:
        if self.is_block():
            return "#"
        if self.is_empty():
            return "_"
        if self.goal:
            return "G"
        return "`"


def parse_input(in_str: str) -> Dict[Point, Machine]:
    machines = {}
    for line in in_str.split("\n"):
        match = PARSE_RE.match(line)
        if match:
            mid = int(match["x"]), int(match["y"])
            machines[mid] = Machine(mid, match["size"], match["used"], match["avail"])
    return machines


def viable_pairs(machines: Dict[Point, Machine]) -> int:
    count = 0
    for comb in permutations(machines.values(), 2):
        a, b = comb
        if a.used != 0 and a.used < b.avail:
            count += 1
    return count


def print_grid(machines: Dict[Point, Machine]):
    maxx = max(x for x, y in machines) + 1
    maxy = max(y for x, y in machines) + 1
    for y in range(maxy):
        print("".join(machines[(x, y)].grid_chr() for x in range(maxx)))


def _dirs(loc: Point) -> Iterable[Point]:
    for point in ((-1, 0), (0, -1), (1, 0), (0, 1)):
        yield loc[0] + point[0], loc[1] + point[1]


def find_path(machines: Dict[Point, Machine], start: Point, target: Point) -> List[Point]:
    breadth_first: List[Tuple[int, Point]] = [(0, start)]
    rev_map: Dict[Point, Optional[Point]] = {start: None}
    while breadth_first:
        prio, loc = heapq.heappop(breadth_first)
        for newloc in _dirs(loc):
            if newloc not in machines or newloc in rev_map or machines[newloc].is_block():
                continue
            if newloc == target:
                rev = []
                while loc is not None:
                    rev.append(loc)
                    loc = rev_map[loc]
                return rev
            if machines[newloc].goal:
                continue
            rev_map[newloc] = loc
            heapq.heappush(breadth_first, (prio + 1, newloc))
    raise NotImplementedError


def find_empty(machines: Dict[Point, Machine]) -> Point:
    for m in machines.values():
        if m.is_empty():
            return m.id


def solve_grid(machines: Dict[Point, Machine]):
    start = (0, 0)
    goal = (max(x for x, y in machines), 0)
    machines[goal].goal = True
    empty = find_empty(machines)
    goal_path = find_path(machines, start, goal)
    move_count = 0
    for loc in goal_path:
        empty_move = find_path(machines, empty, loc)
        move_count += len(empty_move)
        machines[goal].goal = False
        empty, goal = goal, loc
        move_count += 1
        machines[goal].goal = True
    return move_count


if __name__ == "__main__":
    DATA = (FILE_DIR / "day22.input").read_text().strip()
    MACHINES = parse_input(DATA)
    print(viable_pairs(MACHINES))
    print(solve_grid(MACHINES))
