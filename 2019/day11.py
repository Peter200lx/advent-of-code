from pathlib import Path
from typing import NamedTuple

from processor import Processor, ProgramHalt


class D11Processor(Processor):
    def run_on_output_generator_d11(self):
        ip = 0
        first_input = yield
        if self.debug:
            print(f"{id(self)} received {first_input} from yield")
        self.input.append(first_input)
        try:
            while True:
                ip = self.func_by_instruction_pointer(ip)
                if len(self.output) == 2:
                    if self.debug:
                        print(f"{id(self)} yielding out {self.output}")
                    new_input = yield self.output
                    self.output[:] = []
                    if self.debug:
                        print(f"{id(self)} received {new_input} from yield")
                    self.input.append(new_input)
        except ProgramHalt:
            return None


class Point(NamedTuple):
    y: int
    x: int

    def __add__(self, other):
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


def run_bot(program, part2=False):
    bot = D11Processor(program)
    running_bot = bot.run_on_output_generator_d11()
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


def print_hull(hull):
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
