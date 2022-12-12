import heapq
from pathlib import Path
from typing import List, Tuple, NamedTuple, Dict, Set

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


def find_path(start: Pos, end: Pos, ground: Dict[Pos, int]) -> int:
    prio_queue: List[Tuple[int, Pos]] = [(1, start)]
    seen_points: Set[Pos] = {start}
    while prio_queue:
        depth, last_point = heapq.heappop(prio_queue)
        for direc in DIR_MOVES:
            new_point = direc + last_point
            if new_point not in ground:
                continue
            if ground[new_point] - ground[last_point] >= 2:
                continue
            if new_point == end:
                return depth
            if new_point in seen_points:
                continue
            seen_points.add(new_point)
            heapq.heappush(prio_queue, (depth + 1, new_point))
    return int(9e9)  # Idea from Caleb so None check isn't needed


def find_from_low(end: Pos, ground: Dict[Pos, int]) -> int:
    start_points = [p for p, h in ground.items() if h == ord("a")]
    return min(find_path(s, end, ground) for s in start_points)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    START, END, GROUND = parse_input(DATA)

    print(find_path(START, END, GROUND))
    print(find_from_low(END, GROUND))
