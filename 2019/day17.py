from pathlib import Path
from typing import List, NamedTuple, Dict

from processor import Processor


class Point(NamedTuple):
    y: int
    x: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.y + other.y, self.x + other.x)


ADJACENT = {Point(-1, 0), Point(1, 0), Point(0, 1), Point(0, -1)}


def print_view(scaffold: Dict[Point, str]) -> None:
    maxy = max(p.y for p in scaffold)
    maxx = max(p.x for p in scaffold)
    for row in range(maxy + 1):
        line = [scaffold.get(Point(row, x), "?") for x in range(maxx + 1)]
        print("".join(line))


def cam_out_to_point_cloud(cam_out):
    y = x = 0
    point_cloud = {}
    last_chr = None
    for i, value in enumerate(cam_out):
        character = chr(value)
        if character == "\n":
            if last_chr == "\n":
                return point_cloud, cam_out[i + 1 :]
            x = 0
            y += 1
        else:
            point_cloud[Point(y, x)] = character
            x += 1
        last_chr = character
    raise ValueError("Sequence didn't end in double newline")


def find_scaffold_intersections(point_cloud):
    scaffold = {p for p, c in point_cloud.items() if c == "#"}
    return {p for p in scaffold if sum((p + m) in scaffold for m in ADJACENT) == 4}


def part_1(program: List[int], debug: int = 0):
    running_bot = Processor(program).run_on_input_generator()
    cam_out = next(running_bot)  # Move to first yield for .send(
    point_cloud, _ = cam_out_to_point_cloud(cam_out)
    if debug:
        print_view(point_cloud)
    scaffold_intersect = find_scaffold_intersections(point_cloud)
    return sum(p.y * p.x for p in scaffold_intersect)


PART2_MANUAL_ANALYSIS = """
L,6,L,4,R,8,R,8,L,6,L,4,L,10,R,8,L,6,L,4,R,8,L,4,R,4,L,4,R,8,R,8,L,6,L,4,L,10,
AAAAAAAAAAA CCCCCCCCCCCCCCCCCCCC AAAAAAAAAAA BBBBBBBBBBBBBBB CCCCCCCCCCCCCCCC
R,8,L,4,R,4,L,4,R,8,R,8,L,6,L,4,L,10,R,8,L,4,R,4,L,4,R,8,L,6,L,4,R,8,R,8,L,6,L,4,L,10,R,8
BBBBBBBBBBBBBBB CCCCCCCCCCCCCCCCCCCCCCCC BBBBBBBBBBBBBBB AAAAAAAAAAA CCCCCCCCCCCCCCCCCCCC
............................##4##..........
............................#...#..........
............................#...#..........
............................6...6..........
............................#...#..........
............................#...#..........
........................#########..........
........................#...#..............
........................#...4..............
........................#...#..............
....................#########..............
....................#...#..................
....................4...#..................
....................#...#..................
................##4##...##4##..............
................#...........#..............
..............Z.4...........4.Y............
................#...........#..............
........####8####...........##4##..........
........#.......................#..........
........#.......................#..........
........6.......................#..........
###6###.#...................#8#######......
#.....#.#...................#...#...#......
4.....#.##4##......S........4...#...#......
#.....#.....8...............#...#...#......
###6####4##.#.###6##^...##4##...##4####6###
......#...#.#.4.........#...........#.....#
......#.#########.....X.4...........#.....4
......#.#.#.#.#.........#...........#.....#
......#######8#.####8####...........###6###
........4.#.#...#..........................
....#########...4..........................
....#...#.#.....#..........................
....#...#.###6###..........................
....6...6..................................
....#...#..................................
....#...#..................................
....##4##..................................

S: L,6,L,4,R,8
X: L,6,L,4,R,8,L,4,R,4,L,4,R,8
Y: 8,L,4,R,4,L,4,R,8
Z: L,4,R,4,L,4,R,8,L,6,L,4,R,8

A: L,6,L,4,R,8
B: L,4,R,4,L,4,R,8
C: R,8,L,6,L,4,L,10,R,8
"""


def run_bot(program: List[int], debug: int = 0):
    room = {}
    running_bot = Processor(program, ((0, 2),),).run_on_input_generator()
    cam_out = next(running_bot)  # Move to first yield for .send(
    point_cloud, remaining = cam_out_to_point_cloud(cam_out)
    if debug:
        print_view(point_cloud)
        print("".join(chr(i) for i in remaining), end="")
    main_routine = "A,C,A,B,C,B,C,B,A,C"
    func_a = "L,6,L,4,R,8"
    func_b = "L,4,R,4,L,4,R,8"
    func_c = "R,8,L,6,L,4,L,10,R,8"
    video = "y" if debug > 3 else "n"
    input_str = "\n".join((main_routine, func_a, func_b, func_c, video)) + "\n"
    if debug:
        print(input_str.split("\n", 1)[0])
    try:
        i = 0
        while i < len(input_str):
            output = running_bot.send(ord(input_str[i]))
            i += 1
            if i < len(input_str):
                if debug and len(output) != 0:
                    print("".join(chr(i) for i in output), end="")
                    print(input_str[i:].split("\n", 1)[0])
            else:
                if debug:
                    point_cloud, remaining = cam_out_to_point_cloud(cam_out)
                    print_view(point_cloud)
                    return remaining[0]
                return output[-1]
        raise NotImplementedError(f"Don't expect the bot ask for input again")

    except StopIteration:
        return NotImplementedError(f"Don't expect the bot to ever halt the program")


if __name__ == "__main__":
    DATA = Path("day17.input").read_text().strip()
    int_list = [int(i) for i in DATA.split(",")]

    print(part_1(int_list))
    print(run_bot(int_list))
