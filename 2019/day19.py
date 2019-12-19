from collections import defaultdict
from pathlib import Path
from typing import List, NamedTuple, Dict

from processor import Processor


class Point(NamedTuple):
    y: int
    x: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.y + other.y, self.x + other.x)


def print_view(scan: Dict[Point, int], starty: int = 0, startx: int = 0) -> None:
    maxy = max(p.y for p in scan if scan[p])
    maxx = max(p.x for p in scan if scan[p])
    for row in range(starty, maxy + 1):
        line = [scan.get(Point(row, x), 2) for x in range(startx, maxx + 1)]
        print("".join(" X."[i] for i in line))


def check_location(bot: Processor, program: List[int], point: Point) -> int:
    bot.memory = defaultdict(int, enumerate(program))
    try:
        running_bot = bot.run_on_input_generator()
        next(running_bot)  # Move to first yield for .send(
        running_bot.send(point.x)
        (output,) = running_bot.send(point.y)
        return output

    except StopIteration:
        raise NotImplementedError(f"Don't expect the bot to ever halt the program")


def run_bot(program: List[int]) -> Dict[Point, int]:
    bot = Processor(program)
    points_to_scan = [Point(y, x) for x in range(50) for y in range(50)]
    scan = {}
    for point in points_to_scan:
        scan[point] = check_location(bot, program, point)
    return scan


def find_top_right(scan: Dict[Point, int]) -> Point:
    square_size = max(p.x for p in scan)
    for y in range(square_size):
        p = Point(y, square_size)
        if scan[p]:
            return p
    for x in range(square_size, 0, -1):
        p = Point(square_size, x)
        if scan[p]:
            return p
    raise NotImplementedError("Unable to find beam on far edges of sweep")


RIGHT = Point(0, 1)
DOWN = Point(1, 0)
OPPOSITE_CORNER = Point(99, -99)
RESULT_CORNER = Point(0, -99)


def part_2(program: List[int], scan: Dict[Point, int]) -> Point:
    bot = Processor(program)
    top_edge = find_top_right(scan)
    while True:
        top_edge += RIGHT
        while not check_location(bot, program, top_edge):
            top_edge += DOWN
        check_corner = top_edge + OPPOSITE_CORNER
        if check_corner.x > 0 and check_location(bot, program, check_corner):
            return top_edge + RESULT_CORNER


if __name__ == "__main__":
    DATA = Path("day19.input").read_text().strip()
    int_list = [int(i) for i in DATA.split(",")]

    field = run_bot(int_list)
    print_view(field)
    print(sum(field.values()))
    result = part_2(int_list, field)
    print(result.x * 10_000 + result.y)
