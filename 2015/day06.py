from pathlib import Path
import re
from typing import Tuple, List

import numpy as np

INPUT_FILE = Path(__file__).with_suffix(".input")

TURN_RE = re.compile(r"turn (on|off) (\d+),(\d+) through (\d+),(\d+)")
TOGGLE_RE = re.compile(r"toggle (\d+),(\d+) through (\d+),(\d+)")


def parse_line(line: str) -> Tuple[str, int, int, int, int]:
    match = TURN_RE.match(line)
    if match:
        direction, *coords = match.groups()
        return (direction, *(int(s) for s in coords))
    match = TOGGLE_RE.match(line)
    if match:
        coords = match.groups()
        return ("toggle", *(int(s) for s in coords))
    raise ValueError(f"Input line '{line}' didn't match any regex")


def process_instructions_p1(grid, cmds: List[str]):
    for line in cmds:
        instruction, x1, y1, x2, y2 = parse_line(line)
        if instruction == "on":
            grid[y1 : y2 + 1, x1 : x2 + 1] = 1
        elif instruction == "off":
            grid[y1 : y2 + 1, x1 : x2 + 1] = 0
        elif instruction == "toggle":
            grid[y1 : y2 + 1, x1 : x2 + 1] = np.invert(grid[y1 : y2 + 1, x1 : x2 + 1])
        else:
            raise ValueError(f"Unrecognized instruction '{instruction}'")


def process_instructions_p2(grid, cmds: List[str]):
    for line in cmds:
        instruction, x1, y1, x2, y2 = parse_line(line)
        if instruction == "on":
            grid[y1 : y2 + 1, x1 : x2 + 1] += 1
        elif instruction == "off":
            sub_by_1_down_to_0 = np.vectorize(lambda x: x - 1 if x - 1 >= 0 else 0)
            grid[y1 : y2 + 1, x1 : x2 + 1] = sub_by_1_down_to_0(grid[y1 : y2 + 1, x1 : x2 + 1])
        elif instruction == "toggle":
            grid[y1 : y2 + 1, x1 : x2 + 1] += 2
        else:
            raise ValueError(f"Unrecognized instruction '{instruction}'")


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    grid = np.zeros((1000, 1000), dtype=bool)
    process_instructions_p1(grid, DATA.split("\n"))
    print(np.count_nonzero(grid))
    grid = np.zeros((1000, 1000), dtype=np.uint64)
    process_instructions_p2(grid, DATA.split("\n"))
    print(np.sum(grid))
