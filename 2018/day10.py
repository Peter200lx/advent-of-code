import re
from collections import namedtuple

import numpy as np

EXAMPLE_DATA = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>"""


np.set_printoptions(linewidth=130, formatter={'bool': lambda x: '#' if x else ' '})

Coord = namedtuple('Coord', ['y', 'x'])
Vector = namedtuple('Vect', ['pos', 'vel'])

LINE_PARSE = re.compile(r"position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>")


class Bounds:
    def __init__(self):
        self.miny = None
        self.maxy = None
        self.minx = None
        self.maxx = None

    def update(self, y, x):
        if self.miny is None:
            self.miny = y
            self.maxy = y
            self.minx = x
            self.maxx = x
        else:
            self.miny = min(self.miny, y)
            self.maxy = max(self.maxy, y)
            self.minx = min(self.minx, x)
            self.maxx = max(self.maxx, x)

    @property
    def size(self):
        return self.y * self.x

    @property
    def y(self):
        return self.maxy - self.miny + 1

    @property
    def x(self):
        return self.maxx - self.minx + 1

    def translate(self, loc):
        return Coord(loc.y - self.miny, loc.x - self.minx)


def find_message(instructions):
    bounds = Bounds()
    field = []
    for line in instructions:
        match = LINE_PARSE.match(line)
        py, px, vy, vx = [int(i) for i in match.groups()]
        bounds.update(py, px)
        field.append(Vector(Coord(py, px), Coord(vy, vx)))
    # print_message(field, bounds)
    p2_count = 0
    while True:
        new_field = []
        new_bounds = Bounds()
        for pos, vec in field:
            new_loc = Coord(pos.y + vec.y, pos.x + vec.x)
            new_bounds.update(new_loc.y, new_loc.x)
            new_field.append(Vector(new_loc, vec))
        if new_bounds.size > bounds.size:
            break
        # print_message(new_field, new_bounds)
        p2_count += 1
        field = new_field
        bounds = new_bounds
    print(f"Part 2: {p2_count}")
    return field, bounds


def print_message(field, bounds):
    array = np.zeros((bounds.x, bounds.y), dtype=np.bool)
    for loc in field:
        loc = bounds.translate(loc.pos)
        array[loc.x, loc.y] = True
    print(array)


if __name__ == '__main__':
    with open("day10.input", "r") as in_file:
        DATA = in_file.read().strip("\n")

    message, m_bounds = find_message(DATA.split("\n"))
    print_message(message, m_bounds)
