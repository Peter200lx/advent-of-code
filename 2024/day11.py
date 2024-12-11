from collections import Counter
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

MUL_NUM = 2024
P1_COUNT = 25
P2_COUNT = 75


def solve(values: list[int], iterations: int) -> int:
    stones = Counter(values)
    for i in range(iterations):
        nstones = Counter()
        for stone, count in stones.items():
            if stone == 0:
                nstones[1] += count
                continue
            v_str = f"{stone}"
            if len(v_str) % 2 == 0:
                nstones[int(v_str[: len(v_str) // 2])] += count
                nstones[int(v_str[len(v_str) // 2 :])] += count
                continue
            nstones[stone * MUL_NUM] += count
        stones = nstones
    return sum(stones.values())


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    STONES = [int(n) for n in DATA.split()]

    print(solve(STONES, P1_COUNT))
    print(solve(STONES, P2_COUNT))
