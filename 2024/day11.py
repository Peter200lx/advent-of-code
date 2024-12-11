from collections import Counter
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

MUL_NUM = 2024
P1_COUNT = 25
P2_COUNT = 75


def rules(value: int) -> list[int]:
    if value == 0:
        return [1]
    v_str = f"{value}"
    if len(v_str) % 2 == 0:
        return [int(v_str[: len(v_str) // 2]), int(v_str[len(v_str) // 2 :])]
    return [value * 2024]


def p1(values: list[int]) -> int:
    my_list = list(values)
    for i in range(P1_COUNT):
        my_list = [v for n in my_list for v in rules(n)]
    return len(my_list)


def p2(values: list[int]) -> int:
    stones = Counter(values)
    for i in range(P2_COUNT):
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
            nstones[stone * 2024] += count
        stones = nstones
    return sum(stones.values())


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    STONES = [int(n) for n in DATA.split()]

    print(p1(STONES))
    print(p2(STONES))
