from pathlib import Path
from typing import List, Tuple

INPUT_FILE = Path(__file__).with_suffix(".input")


def solve(items: List[List[int]]) -> Tuple[int, int]:
    p1 = p2 = 0
    for e1, e2 in items:
        s1, s2 = set(range(e1[0], e1[1] + 1)), set(range(e2[0], e2[1] + 1))
        comb = s1 & s2
        p1 += len(comb) == min(len(s1), len(s2))
        p2 += 1 if comb else 0
    return p1, p2


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT_DATA = [
        [[int(i) for i in pair.split("-")] for pair in line.split(",")]
        for line in DATA.split("\n")
    ]

    print(solve(INPUT_DATA))
