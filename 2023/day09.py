from pathlib import Path
from typing import List

INPUT_FILE = Path(__file__).with_suffix(".input")


def solve_line(nums: List[int]) -> int:
    deltas = [nums[i] - nums[i - 1] for i in range(1, len(nums))]
    if all(n == 0 for n in deltas):
        return 0
    return deltas[-1] + solve_line(deltas)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    LINES = [[int(n) for n in line.split()] for line in DATA.splitlines()]

    print(sum(line[-1] + solve_line(line) for line in LINES))
    print(sum(line[0] + solve_line(line[::-1]) for line in LINES))
