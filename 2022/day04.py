from pathlib import Path
from typing import List

INPUT_FILE = Path(__file__).with_suffix(".input")


def part1(e1: List[int], e2: List[int]) -> bool:
    s1, s2 = set(range(e1[0], e1[1] + 1)), set(range(e2[0], e2[1] + 1))
    if len(s1) > len(s2):
        return s1 & s2 == s2
    return s1 & s2 == s1


def part2(e1: List[int], e2: List[int]) -> bool:
    s1, s2 = set(range(e1[0], e1[1] + 1)), set(range(e2[0], e2[1] + 1))
    return bool(s1 & s2)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT_DATA = [
        [[int(i) for i in pair.split("-")] for pair in line.split(",")]
        for line in DATA.split("\n")
    ]

    print(sum(part1(*l) for l in INPUT_DATA))
    print(sum(part2(*l) for l in INPUT_DATA))
