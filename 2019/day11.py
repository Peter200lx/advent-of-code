from pathlib import Path
from typing import NamedTuple, Dict, List

from processor import Processor


class Point(NamedTuple):
    y: int
    x: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.y + other.y, self.x + other.x)


DIR_VEC = {
    "^": Point(-1, 0),
    "v": Point(1, 0),
    ">": Point(0, 1),
    "<": Point(0, -1),
}

TURN_DB = {
    "^": {0: "<", 1: ">"},
    "v": {0: ">", 1: "<"},
    "<": {0: "v", 1: "^"},
    ">": {0: "^", 1: "v"},
}


def run_bot(program: List[int], part2: bool = False) -> Dict[Point, int]:
    bot = Processor(program)
    running_bot = bot.run_on_output_generator(output_batch=2)
    next(running_bot)
    location = Point(0, 0)
    if not part2:
        hull = {}
    else:
        hull = {location: 1}
    direction = "^"
    try:
        while True:
            color = hull.get(location, 0)
            new_color, turn = running_bot.send(color)
            hull[location] = new_color
            direction = TURN_DB[direction][turn]
            location = location + DIR_VEC[direction]
    except StopIteration:
        return hull


def print_hull(hull: Dict[Point, int]) -> None:
    miny = min(p.y for p in hull)
    maxy = max(p.y for p in hull)
    minx = min(p.x for p in hull)
    maxx = max(p.x for p in hull)
    for row in range(miny, maxy + 1):
        line = (hull.get(Point(row, x), 0) for x in range(minx, maxx + 1))
        print("".join("#" if i else " " for i in line))


if __name__ == "__main__":
    DATA = Path("day11.input").read_text().strip()
    int_list = [int(i) for i in DATA.split(",")]

    print(len(run_bot(int_list)))
    field = run_bot(int_list, part2=True)
    print_hull(field)
