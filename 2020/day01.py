from itertools import permutations
from math import prod
from pathlib import Path

FILE_DIR = Path(__file__).parent


def find_matching_sum(input_list, sum_to, n):
    for perm in permutations(input_list, n):
        if sum(perm) == sum_to:
            return perm


if __name__ == "__main__":
    DATA = (FILE_DIR / "day01.input").read_text().strip()
    INPUT_INTS = [int(i) for i in DATA.split("\n")]
    MATCH_NUM = 2020

    print(prod(find_matching_sum(INPUT_INTS, MATCH_NUM, 2)))
    print(prod(find_matching_sum(INPUT_INTS, MATCH_NUM, 3)))
