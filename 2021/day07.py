from pathlib import Path
from statistics import mean, median
from typing import List

INPUT_FILE = Path(__file__).with_suffix(".input")


def part1(sub_pos: List[int]) -> int:
    mid_crab = int(median(sub_pos))
    return sum(abs(pos - mid_crab) for pos in sub_pos)


def part2(sub_pos: List[int]) -> int:
    mid_pos = int(mean(sub_pos))
    return min(
        sum(sum(range(1, abs(pos - to_check) + 1)) for pos in sub_pos)
        for to_check in range(mid_pos - 1, mid_pos + 1)
    )


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    POSITIONS = [int(line) for line in DATA.split(",")]
    print(part1(POSITIONS))
    print(part2(POSITIONS))
