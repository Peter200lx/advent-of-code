import re
from pathlib import Path
from typing import NamedTuple, Tuple, Union, List

INPUT_FILE = Path(__file__).with_suffix(".input")

RE_NUMS = re.compile(r"-?\d+")


class Target(NamedTuple):
    x_range: Tuple[int, int]
    y_range: Tuple[int, int]

    @staticmethod
    def from_str(in_str: str) -> "Target":
        xmin, xmax, ymin, ymax = tuple(map(int, RE_NUMS.findall(in_str)))
        return Target((xmin, xmax), (ymin, ymax))


def fire_probe(target: Target, xvel: int, yvel: int, p2=False) -> Union[bool, int]:
    xloc = yloc = ymax = 0
    while xloc < target.x_range[1] and yloc > target.y_range[0]:
        xloc, yloc = xloc + xvel, yloc + yvel
        ymax = max(ymax, yloc)
        yvel -= 1
        if xvel > 0:
            xvel -= 1
        if (
            target.x_range[0] <= xloc <= target.x_range[1]
            and target.y_range[0] <= yloc <= target.y_range[1]
        ):
            return True if p2 else ymax
    return False


def find_x_values(target: Target, only_stall: bool = False) -> List[int]:
    possible_x = []
    for x in range(1, target.x_range[1] + 1):
        xvel = x
        xloc = 0
        while xvel > 0 and xloc <= target.x_range[1]:
            xloc += xvel
            xvel -= 1
            if target.x_range[0] <= xloc <= target.x_range[1]:
                if only_stall and xvel == 0:
                    return [x]
                possible_x.append(x)
                break
    return possible_x


def part1(target: Target) -> int:
    x = find_x_values(target, only_stall=True)[0]
    return max(fire_probe(target, x, y) for y in range(1, 100))


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    TARGET = Target.from_str(DATA)

    print(part1(TARGET))
    print(
        sum(
            fire_probe(TARGET, x, y, p2=True)
            for x in find_x_values(TARGET)
            for y in range(-abs(TARGET.y_range[0]), abs(TARGET.y_range[0]))
        )
    )
