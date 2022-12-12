import heapq
from pathlib import Path
from typing import List, Tuple, NamedTuple, Dict

INPUT_FILE = Path(__file__).with_suffix(".input")


class Pos(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Pos") -> "Pos":
        return Pos(self.x + other.x, self.y + other.y)


DIR_MOVES = [Pos(0, 1), Pos(0, -1), Pos(-1, 0), Pos(1, 0)]


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


def find_path(end: Pos, ground: Dict[Pos, int]) -> Dict[Pos, int]:
    prio_queue: List[Tuple[int, Pos]] = [(0, end)]
    cost_to_point: Dict[Pos, int] = {end: 0}
    while prio_queue:
        depth, last_point = heapq.heappop(prio_queue)
        for direc in DIR_MOVES:
            new_point = direc + last_point
            if new_point not in ground:
                continue
            if ground[last_point] - ground[new_point] >= 2:
                continue
            if new_point in cost_to_point:
                continue
            cost_to_point[new_point] = depth + 1
            heapq.heappush(prio_queue, (depth + 1, new_point))
    return cost_to_point


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    START, END, GROUND = parse_input(DATA)

    POINT_COSTS = find_path(END, GROUND)
    print(POINT_COSTS[START])
    print(min(POINT_COSTS[point] for point in POINT_COSTS if GROUND[point] == ord("a")))
