from pathlib import Path
from typing import List

INPUT_FILE = Path(__file__).with_suffix(".input")


def solve_line(nums: List[int]) -> int:
    deltas = []
    for i, n in enumerate(nums):
        if i == 0:
            continue
        deltas.append(n - nums[i - 1])
    if all(n == 0 for n in deltas):
        return 0
    return deltas[-1] + solve_line(deltas)


def solve_line2(nums: List[int]) -> int:
    deltas = []
    for i, n in enumerate(nums):
        if i == 0:
            continue
        deltas.append(n - nums[i - 1])
    if all(n == 0 for n in deltas):
        return 0
    return deltas[0] - solve_line2(deltas)


def part_one(lines: List[List[int]]) -> int:
    next_nums = []
    for line in lines:
        next_nums.append(line[-1] + solve_line(line))
    return sum(next_nums)


def part_two(lines: List[List[int]]) -> int:
    next_nums = []
    for line in lines:
        next_nums.append(line[0] - solve_line2(line))
    return sum(next_nums)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    LINES = [[int(n) for n in line.split()] for line in DATA.splitlines()]

    print(part_one(LINES))
    print(part_two(LINES))
