from pathlib import Path
from typing import List

INPUT_FILE = Path(__file__).with_suffix(".input")


def solve_line(nums: List[int], p1: bool = True) -> int:
    deltas = []
    for i, n in enumerate(nums):
        if i == 0:
            continue
        deltas.append(n - nums[i - 1])
    if all(n == 0 for n in deltas):
        return 0
    if p1:
        return deltas[-1] + solve_line(deltas, p1)
    else:
        return deltas[0] - solve_line(deltas, p1)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    LINES = [[int(n) for n in line.split()] for line in DATA.splitlines()]

    print(sum(line[-1] + solve_line(line) for line in LINES))
    print(sum(line[0] - solve_line(line, p1=False) for line in LINES))
