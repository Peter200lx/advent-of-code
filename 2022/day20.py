from pathlib import Path
from typing import List

INPUT_FILE = Path(__file__).with_suffix(".input")


GROOVES = [1000, 2000, 3000]
KEY = 811589153
P2_COUNT = 10


def solve(seq: List[int], count: int = 1) -> int:
    moved_list = [i for i in range(len(seq))]
    for n in list(moved_list) * count:
        i = moved_list.index(n)
        moved_list.pop(i)
        new_index = (seq[n] + i) % len(moved_list)
        if new_index == 0:
            moved_list.append(n)
        else:
            moved_list.insert(new_index, n)
    zero_index = moved_list.index(seq.index(0))
    grooves = [seq[moved_list[(i + zero_index) % len(moved_list)]] for i in GROOVES]
    return sum(grooves)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    CODE = [int(line) for line in DATA.split("\n")]

    print(solve(CODE))
    print(solve([i * KEY for i in CODE], 10))
