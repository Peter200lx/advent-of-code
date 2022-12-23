from collections import defaultdict
from pathlib import Path
from typing import List, NamedTuple, Set, Tuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Pos(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Pos") -> "Pos":
        return Pos(self.x + other.x, self.y + other.y)


ALL_AROUND = [
    Pos(x, y) for x in range(-1, 2) for y in range(-1, 2) if not (x == 0 and y == 0)
]

MOVES = [
    ((Pos(0, -1), Pos(1, -1), Pos(-1, -1)), Pos(0, -1)),
    ((Pos(0, 1), Pos(1, 1), Pos(-1, 1)), Pos(0, 1)),
    ((Pos(-1, 0), Pos(-1, -1), Pos(-1, 1)), Pos(-1, 0)),
    ((Pos(1, 0), Pos(1, -1), Pos(1, 1)), Pos(1, 0)),
]


def parse(raw_str: str) -> Set[Pos]:
    cloud = set()
    for y, line in enumerate(raw_str.split("\n")):
        for x, c in enumerate(line):
            if c == "#":
                cloud.add(Pos(x, y))
    return cloud


def run_step(prev_state: Set[Pos], rnd: int) -> Set[Pos]:
    proposed: defaultdict[Pos, List[Pos]] = defaultdict(list)
    for point in prev_state:
        if all((point + p) not in prev_state for p in ALL_AROUND):
            proposed[point].append(point)
            continue
        for i in range(4):
            req, res = MOVES[(i + rnd) % 4]
            if all((point + d) not in prev_state for d in req):
                proposed[point + res].append(point)
                break
        else:
            proposed[point].append(point)
    result = {p for p, l in proposed.items() if len(l) == 1}
    return result | {p for l in proposed.values() for p in l if len(l) > 1}


def print_elves(elves: Set[Pos]):
    min_x, max_x = min(p.x for p in elves), max(p.x for p in elves)
    min_y, max_y = min(p.y for p in elves), max(p.y for p in elves)
    print(f"{min_x=} {max_x=}  {min_y=} {max_y=}")
    for y in range(min_y, max_y + 1):
        print(
            "".join("#" if Pos(x, y) in elves else "." for x in range(min_x, max_x + 1))
        )
    print("")


def solve(initial: Set[Pos]) -> Tuple[int, int]:
    cur_state = set(initial)
    for i in range(10):
        cur_state = run_step(cur_state, i)
        # print_elves(cur_state)
    min_x, max_x = min(p.x for p in cur_state), max(p.x for p in cur_state)
    min_y, max_y = min(p.y for p in cur_state), max(p.y for p in cur_state)
    part1 = (max_x - min_x + 1) * (max_y - min_y + 1) - len(cur_state)

    for i in range(10, 5000):
        next_state = run_step(cur_state, i)
        if next_state == cur_state:
            break
        cur_state = next_state
    return part1, i + 1


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().rstrip()
    INITIAL = parse(DATA)

    print(solve(INITIAL))
