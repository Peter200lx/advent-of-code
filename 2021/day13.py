from pathlib import Path
from typing import NamedTuple, Tuple, Set, List

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int


class Inst(NamedTuple):
    line: str  # x or y
    value: int


def parse_input(in_str: str) -> Tuple[Set[Coord], List[Inst]]:
    dotstr, inststr = in_str.split("\n\n")
    return {
        Coord(int(x), int(y))
        for line in dotstr.split("\n")
        for x, y in [line.split(",")]
    }, [
        Inst(d, int(n))
        for line in inststr.split("\n")
        for d, n in [line.split()[-1].split("=")]
    ]


def flip(loc: int, amount: int) -> int:
    return amount - (loc - amount)


def solve(dots: Set[Coord], instructions: List[Inst]):
    p1 = False
    for inst in instructions:
        if inst.line == "x":
            dots = {
                Coord(flip(dot.x, inst.value), dot.y) if dot.x > inst.value else dot
                for dot in dots
            }
        elif inst.line == "y":
            dots = {
                Coord(dot.x, flip(dot.y, inst.value)) if dot.y > inst.value else dot
                for dot in dots
            }
        if not p1:
            print(len(dots))
            p1 = True
    print_dots(dots)


def print_dots(dots):
    minx, maxx = min(dot.x for dot in dots), max(dot.x for dot in dots)
    miny, maxy = min(dot.y for dot in dots), max(dot.y for dot in dots)
    for y in range(miny, maxy + 1):
        print("".join("#" if (x, y) in dots else " " for x in range(minx, maxx + 1)))


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    THERMAL_MAP, INSTRUCTIONS = parse_input(DATA)
    solve(THERMAL_MAP, INSTRUCTIONS)
