import statistics
from pathlib import Path
from typing import List

FILE_DIR = Path(__file__).parent


def part1(sub_pos: List[int]) -> int:
    mean = int(statistics.median(sub_pos))
    return sum(abs(pos - mean) for pos in sub_pos)


def part2(sub_pos: List[int]) -> int:
    mid = int(statistics.mean(sub_pos))
    return min(
        sum(sum(range(1, abs(pos - to_check) + 1)) for pos in sub_pos)
        for to_check in range(mid - 1, mid + 1)
    )


if __name__ == "__main__":
    DATA = (FILE_DIR / "day07.input").read_text().strip()
    POSITIONS = [int(line) for line in DATA.split(",")]
    print(part1(POSITIONS))
    print(part2(POSITIONS))
