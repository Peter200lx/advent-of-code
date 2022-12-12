import heapq
from pathlib import Path
from typing import List, Tuple, NamedTuple, Dict, Optional

INPUT_FILE = Path(__file__).with_suffix(".input")


class Pos(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Pos") -> "Pos":
        return Pos(self.x + other.x, self.y + other.y)


DIR_MOVES = [
    Pos(0, 1),
    Pos(0, -1),
    Pos(-1, 0),
    Pos(1, 0),
]


def parse_input(instr: str):
    start = end = None
    ground = {}
    for y, line in enumerate(instr.split("\n")):
        for x, c in enumerate(line):
            if c == "S":
                start = Pos(x, y)
                ground[start] = ord("a")
            elif c == "E":
                end = Pos(x, y)
                ground[end] = ord("z")
            else:
                ground[Pos(x, y)] = ord(c)
    return start, end, ground


def find_path(start: Pos, end: Pos, ground: Dict[Pos, int]) -> Optional[int]:
    prio_queue: List[Tuple[int, List[Pos]]] = [(0, [start])]
    seen_points: Dict[Pos, int] = {start: 0}
    while prio_queue:
        prio, so_far = heapq.heappop(prio_queue)
        for direc in DIR_MOVES:
            last_point = so_far[-1]
            new_point = direc + last_point
            if new_point not in ground:
                continue
            if ground[new_point] - ground[last_point] >= 2:
                continue
            if new_point == end:
                return len(so_far)
            new_cost = prio + 1
            if seen_points.get(new_point, 9e9) <= new_cost:
                continue
            seen_points[new_point] = new_cost
            heapq.heappush(prio_queue, (new_cost, so_far + [new_point]))


def find_from_low(end: Pos, ground: Dict[Pos, int]):
    start_points = [p for p, h in ground.items() if h == ord("a")]
    possible = [find_path(s, end, ground) for s in start_points]
    return min(p for p in possible if p)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    START, END, GROUND = parse_input(DATA)

    print(find_path(START, END, GROUND))
    print(find_from_low(END, GROUND))
