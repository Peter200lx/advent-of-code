from itertools import combinations
from math import ceil, floor
from pathlib import Path
from typing import List, Union

INPUT_FILE = Path(__file__).with_suffix(".input")

SnailfishLine = List[Union[str, int]]


def explode(line: SnailfishLine):
    depth = 0
    for i, item in enumerate(line):
        if item == "[":
            depth += 1
            if depth >= 5:
                to_ex_l, to_ex_r = line[i + 1 : i + 3]
                for j in range(i + 3, len(line)):
                    if isinstance(line[j], int):
                        line[j] += to_ex_r
                        break
                for k in range(i - 1, 0, -1):
                    if isinstance(line[k], int):
                        line[k] += to_ex_l
                        break
                line[i : i + 4] = [0]
                depth -= 1
        elif item == "]":
            depth -= 1


def split(line: SnailfishLine) -> bool:
    for i, item in enumerate(line):
        if isinstance(item, int) and item >= 10:
            half = item / 2
            line[i : i + 1] = ["[", floor(half), ceil(half), "]"]
            return True


def reduce(line: SnailfishLine):
    while True:
        explode(line)
        if split(line):
            continue
        return line


def part1(lines: List[SnailfishLine]) -> SnailfishLine:
    so_far, *lines = lines
    for line in lines:
        so_far = reduce(["["] + so_far + line + ["]"])
    return so_far


def calc_magnitude(data: SnailfishLine) -> int:
    nested: List[List[int]] = []
    for i, item in enumerate(data):
        if item == "[":
            nested.append([])
        elif item == "]":
            current = nested.pop(-1)
            if nested:
                nested[-1].append(3 * current[0] + 2 * current[1])
            else:
                return 3 * current[0] + 2 * current[1]
        else:
            nested[-1].append(item)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    SNAILFISH_ARRAY = [
        [int(c) if c.isdigit() else c for c in line if c != ","]
        for line in DATA.split("\n")
    ]

    print(calc_magnitude(part1(SNAILFISH_ARRAY)))
    print(
        max(
            calc_magnitude(reduce(["["] + left + right + ["]"]))
            for left, right in combinations(SNAILFISH_ARRAY, 2)
        )
    )
