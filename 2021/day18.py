import re
from ast import literal_eval
from itertools import combinations
from math import ceil, floor
from pathlib import Path
from typing import List, Optional

RE_NUMS = re.compile(r"-?\d+")

INPUT_FILE = Path(__file__).with_suffix(".input")


def explode(line: str) -> Optional[str]:
    depth = 0
    for i, c in enumerate(line):
        if c == "[":
            depth += 1
            if depth >= 5:
                right_bracket = line.find("]", i)
                to_explode = line[i + 1 : right_bracket]
                line = line[:i] + "0" + line[right_bracket + 1 :]
                left_num = right_num = None
                for match in RE_NUMS.finditer(line):
                    if match.start() < i:
                        left_num = match
                    elif match.start() > i:
                        right_num = match
                        break
                to_ex_l, to_ex_r = map(int, to_explode.split(","))
                if left_num and right_num:
                    line = (
                        line[: left_num.start()]
                        + f"{to_ex_l + int(left_num.group(0))}"
                        + line[left_num.end() : right_num.start()]
                        + f"{to_ex_r + int(right_num.group(0))}"
                        + line[right_num.end() :]
                    )
                elif left_num:
                    line = (
                        line[: left_num.start()]
                        + f"{to_ex_l + int(left_num.group(0))}"
                        + line[left_num.end() :]
                    )
                elif right_num:
                    line = (
                        line[: right_num.start()]
                        + f"{to_ex_r + int(right_num.group(0))}"
                        + line[right_num.end() :]
                    )
                return line
        elif c == "]":
            depth -= 1


def split(line: str) -> Optional[str]:
    for match in RE_NUMS.finditer(line):
        value = int(match.group(0))
        if value >= 10:
            half = value / 2
            return (
                line[: match.start()]
                + f"[{floor(half)},{ceil(half)}]"
                + line[match.end() :]
            )


def reduce(line: str):
    while True:
        if line_exp := explode(line):
            line = line_exp
            continue
        if line_split := split(line):
            line = line_split
            continue
        return line


def part1(lines: List[str]):
    so_far, *lines = lines
    for line in lines:
        so_far = reduce(f"[{so_far},{line}]")
    return so_far


def calc_magnitude(data: str) -> int:
    if isinstance(data, str):
        data = literal_eval(data)
    if isinstance(data, int):
        return data
    if isinstance(data, list):
        return 3 * calc_magnitude(data[0]) + 2 * calc_magnitude(data[1])


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    SNAILFISH_ARRAY = [line for line in DATA.split("\n")]

    print(calc_magnitude(part1(SNAILFISH_ARRAY)))
    print(
        max(
            calc_magnitude(reduce(f"[{left},{right}]"))
            for left, right in combinations(SNAILFISH_ARRAY, 2)
        )
    )
