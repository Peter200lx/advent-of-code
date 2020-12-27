from collections import defaultdict
from pathlib import Path
from typing import NamedTuple, Set

FILE_DIR = Path(__file__).parent


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def valid(self):
        return 0 <= self.x < 100 and 0 <= self.y < 100


NEIGHBORS = {Point(x, y) for x in range(-1, 2) for y in range(-1, 2) if (x, y) != (0, 0)}
STUCK_CORNERS = {Point(0, 0), Point(0, 99), Point(99, 0), Point(99, 99)}


def parse_input(input_text: str) -> Set[Point]:
    points = set()
    for y, line in enumerate(input_text.split("\n")):
        for x, c in enumerate(line):
            if c == "#":
                points.add(Point(x=x, y=y))
    return points


def next_state(is_on: bool, neighbor_count: int):
    if is_on and neighbor_count in (2, 3):
        return True
    if not is_on and neighbor_count == 3:
        return True
    return False


def run_loops(start: Set[Point], num_iterations: int = 100, part_2: bool = False) -> Set[Point]:
    cur = start
    for _ in range(num_iterations):
        neighbor_counts = defaultdict(int)
        for point in (p + d for p in cur for d in NEIGHBORS):
            if not point.valid():
                continue
            neighbor_counts[point] += 1
        cur = {p for p in neighbor_counts if next_state(p in cur, neighbor_counts[p])}
        if part_2:
            cur |= STUCK_CORNERS
    return cur


if __name__ == "__main__":
    DATA = (FILE_DIR / "day18.input").read_text().strip()
    POINTS = parse_input(DATA)
    print(len(run_loops(POINTS)))
    print(len(run_loops(POINTS, part_2=True)))
