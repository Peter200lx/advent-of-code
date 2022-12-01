from pathlib import Path
from typing import List

INPUT_FILE = Path(__file__).with_suffix(".input")


def count_elves(input_list: List[List[int]]) -> List[int]:
    return [sum(elf) for elf in input_list]


def top_n_sum(input_list: List[int], num: int = 3) -> int:
    input_list.sort(reverse=True)
    return sum(input_list[:num])


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT_ELVES = [[int(i) for i in l.split("\n")] for l in DATA.split("\n\n")]

    print(max(count_elves(INPUT_ELVES)))

    print(top_n_sum(count_elves(INPUT_ELVES)))
