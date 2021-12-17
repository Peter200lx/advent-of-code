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
    xloc, yloc = 0, 0
    ymax = 0
    while xloc < target.x_range[1] and yloc > target.y_range[0]:
        xloc, yloc = xloc + xvel, yloc + yvel
        ymax = max(ymax, yloc)
        yvel -= 1
        if xvel > 0:
            xvel -= 1
        elif xvel < 0:
            xvel += 1
        if (
            target.x_range[0] <= xloc <= target.x_range[1]
            and target.y_range[0] <= yloc <= target.y_range[1]
        ):
            return True if p2 else ymax
    return False


def find_x_values(target: Target, only_stall: bool = True) -> List[int]:
    possible_x = []
    for x in range(1, 999):
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
    x = find_x_values(target)[0]
    max_y = 0
    for y in range(1, 100):
        attempt = fire_probe(target, x, y)
        if attempt:
            max_y = attempt
    return max_y


def part2(target: Target) -> int:
    possible_x = find_x_values(target, only_stall=False)
    viable_coords = []
    for x in possible_x:
        for y in range(-100, 100):
            if fire_probe(target, x, y, p2=True):
                viable_coords.append((x, y))
    return len(viable_coords)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    TARGET = Target.from_str(DATA)

    print(part1(TARGET))
    print(part2(TARGET))
