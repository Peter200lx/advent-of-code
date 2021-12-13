from pathlib import Path
from typing import NamedTuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)


class Inst(NamedTuple):
    line: str  # x or y
    value: int


def parse_input(in_str: str):
    dotstr, inststr = in_str.split("\n\n")
    dots = {
        Coord(int(x), int(y))
        for line in dotstr.split("\n")
        for x, y in [line.split(",")]
    }
    insts = [
        Inst(d, int(n))
        for line in inststr.split("\n")
        for d, n in [line.split()[-1].split("=")]
    ]
    return dots, insts


def solve(dots, instructions):
    p1 = False
    for inst in instructions:
        if inst.line == "x":
            dots = {
                Coord(inst.value - (dot.x - inst.value), dot.y)
                if dot.x > inst.value
                else dot
                for dot in dots
            }
        elif inst.line == "y":
            dots = {
                Coord(dot.x, inst.value - (dot.y - inst.value))
                if dot.y > inst.value
                else dot
                for dot in dots
            }
        if not p1:
            print(len(dots))
            p1 = True
    print_dots(dots)


def print_dots(dots):
    minx = min(dot.x for dot in dots)
    maxx = max(dot.x for dot in dots)
    miny = min(dot.y for dot in dots)
    maxy = max(dot.y for dot in dots)
    for y in range(miny, maxy + 1):
        print("".join("#" if (x, y) in dots else "." for x in range(minx, maxx + 1)))


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    THERMAL_MAP, INSTRUCTIONS = parse_input(DATA)
    solve(THERMAL_MAP, INSTRUCTIONS)
