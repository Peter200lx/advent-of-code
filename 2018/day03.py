import re
from collections import namedtuple

import numpy as np

EXAMPLE_DATA = """#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2"""

re_line = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
Instruction = namedtuple('inst', ['num', 'start', 'size'])
Location = namedtuple('loc', ['y', 'x'])

SIZE = 1000


def parse_line(line):
    match = re_line.match(line)
    assert match
    return Instruction(int(match.group(1)), Location(int(match.group(2)), int(match.group(3))),
                       Location(int(match.group(4)), int(match.group(5))))


def add_square(base, start, size):
    base[start.y:start.y+size.y, start.x:start.x+size.x] += 1


def overlaps(base, instruction):
    start = instruction.start
    size = instruction.size
    if base[start.y:start.y+size.y, start.x:start.x+size.x].sum() == size.x * size.y:
        print(instruction.num)


if __name__ == '__main__':
    with open("day03.input", "r") as in_file:
        DATA = in_file.read().strip("\n")

    list_o_squares = DATA.split("\n")
    world = np.zeros((SIZE, SIZE), dtype=np.int64)
    for inst in (parse_line(l) for l in list_o_squares):
        add_square(world, inst.start, inst.size)
    print((world > 1).sum())
    for inst in (parse_line(l) for l in list_o_squares):
        overlaps(world, inst)
