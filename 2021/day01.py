from pathlib import Path
from typing import List

INPUT_FILE = Path(__file__).with_suffix(".input")


def count_inc(input_list: List[int]) -> int:
    # Great use of int(True) == 1 and zip from
    #  https://www.reddit.com/r/adventofcode/comments/r66vow/comment/hmrfyu8
    return sum(n > p for p, n in zip(input_list, input_list[1:]))


def sliding_window(input_list: List[int], window_size: int = 3) -> List[int]:
    return [
        sum(input_list[i - window_size : i])
        for i in range(window_size, len(input_list) + 1)
    ]


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT_INTS = [int(i) for i in DATA.split("\n")]

    print(count_inc(INPUT_INTS))

    print(count_inc(sliding_window(INPUT_INTS)))
