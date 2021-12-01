from pathlib import Path
from typing import List

FILE_DIR = Path(__file__).parent


def count_inc(input_list: List[int]) -> int:
    # Great use of int(True) == 1 and zip from
    #  https://www.reddit.com/r/adventofcode/comments/r66vow/comment/hmrfyu8
    return sum(n > p for p, n in zip(input_list, input_list[1:]))


def sliding_window(input_list: List[int], window_size: int = 3) -> List[int]:
    sliding_counts = []
    for i, _n in enumerate(input_list):
        try:
            sliding_counts.append(sum(input_list[i : i + window_size]))
        except KeyError:
            break
    return sliding_counts


if __name__ == "__main__":
    DATA = (FILE_DIR / "day01.input").read_text().strip()
    INPUT_INTS = [int(i) for i in DATA.split("\n")]

    print(count_inc(INPUT_INTS))

    print(count_inc(sliding_window(INPUT_INTS)))
