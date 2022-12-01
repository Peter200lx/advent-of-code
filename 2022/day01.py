from pathlib import Path
from typing import List

INPUT_FILE = Path(__file__).with_suffix(".input")


def count_elves(elf_list: List[List[int]]) -> List[int]:
    return [sum(elf) for elf in elf_list]


def top_n_sum(elf_list: List[int], num: int = 3) -> int:
    return sum(sorted(elf_list, reverse=True)[:num])


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT_ELVES = [[int(i) for i in elf.split("\n")] for elf in DATA.split("\n\n")]

    print(max(count_elves(INPUT_ELVES)))

    print(top_n_sum(count_elves(INPUT_ELVES)))
