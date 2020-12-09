from pathlib import Path
from itertools import combinations

FILE_DIR = Path(__file__).parent

PREAMBLE_LEN = 25


def invalid_number(to_check):
    for i, n in enumerate(to_check):
        if i < PREAMBLE_LEN:
            continue
        for comb in combinations(to_check[i - PREAMBLE_LEN : i], 2):
            if sum(comb) == n:
                break
        else:
            return n


def find_sum(to_check, match):
    start_point = 0
    for i, _ in enumerate(to_check):
        while (sum(to_check[start_point : i + 1])) > match:
            start_point += 1
        sequence = to_check[start_point : i + 1]
        if sum(sequence) == match:
            return min(sequence) + max(sequence)


if __name__ == "__main__":
    DATA = (FILE_DIR / "day09.input").read_text().strip()
    NUMBERS = [int(i) for i in DATA.split("\n")]
    invalid = invalid_number(NUMBERS)
    print(invalid)
    print(find_sum(NUMBERS, invalid))
