from collections import defaultdict
from pathlib import Path
from typing import List, NamedTuple, Dict

from processor import Processor


class Point(NamedTuple):
    y: int
    x: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.y + other.y, self.x + other.x)


def print_view(scan: Dict[Point, int], starty=0, startx=0) -> None:
    maxy = max(p.y for p in scan if scan[p])
    maxx = max(p.x for p in scan if scan[p])
    for row in range(starty, maxy + 1):
        line = [scan.get(Point(row, x), 2) for x in range(startx, maxx + 1)]
        print("".join(" X."[i] for i in line))


def run_bot(program: List[int]):
    points_to_scan = [Point(y, x) for x in range(50) for y in range(50)]
    scan = {}
    try:
        for point in points_to_scan:
            running_bot = Processor(program).run_on_input_generator()
            next(running_bot)  # Move to first yield for .send(
            running_bot.send(point.x)
            (output,) = running_bot.send(point.y)
            scan[point] = output
        return scan

    except StopIteration:
        raise NotImplementedError(f"Don't expect the bot to ever halt the program")


def check_location(bot: Processor, program, point: Point):
    bot.memory = defaultdict(int, enumerate(program))
    try:
        running_bot = bot.run_on_input_generator()
        next(running_bot)  # Move to first yield for .send(
        running_bot.send(point.x)
        (output,) = running_bot.send(point.y)
        return output

    except StopIteration:
        raise NotImplementedError(f"Don't expect the bot to ever halt the program")


RIGHT = Point(0, 1)
DOWN = Point(1, 0)
OPPOSITE_CORNER = Point(99, -99)
RESULT_CORNER = Point(0, -99)


def part_2(program: List[int], scan):
    bot = Processor(program)
    start_point = Point(0, 0)
    maxx = max(p.x for p in scan)
    for y in range(maxx):
        p = Point(y, maxx)
        if scan[p]:
            start_point = p
    top_edge = start_point
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
    print(sum(i == 1 for i in field.values()))
    result = part_2(int_list, field)
    print(result.x * 10_000 + result.y)
