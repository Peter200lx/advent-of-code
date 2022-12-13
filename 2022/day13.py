from ast import literal_eval
from pathlib import Path
from typing import List, Optional

INPUT_FILE = Path(__file__).with_suffix(".input")

DIVIDER_PACKETS = [
    [[2]],
    [[6]],
]


def compare(left, right) -> Optional[bool]:
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        return left < right
    if isinstance(left, list) and isinstance(right, list):
        for i, l_val in enumerate(left):
            try:
                r_val = right[i]
            except IndexError:
                return False
            if (ret := compare(l_val, r_val)) is None:
                continue
            return ret
        if len(left) == len(right):
            return None
        return True
    if isinstance(left, int):
        return compare([left], right)
    elif isinstance(right, int):
        return compare(left, [right])
    raise NotImplementedError


def parse(data: List[List[str]]) -> int:
    valid_pairs = []
    for i, (left_str, right_str) in enumerate(data, start=1):
        if compare(literal_eval(left_str), literal_eval(right_str)):
            valid_pairs.append(i)
    return sum(valid_pairs)


class Comparable:
    def __init__(self, obj):
        self.obj = obj

    def __lt__(self, other):
        return compare(self.obj, other.obj)


def full_sort(data: List[List[str]]) -> int:
    parsed_data = [literal_eval(item) for pair in data for item in pair]
    parsed_data.extend(DIVIDER_PACKETS)
    parsed_data.sort(key=lambda x: Comparable(x))
    div_loc = [parsed_data.index(d) + 1 for d in DIVIDER_PACKETS]
    return div_loc[0] * div_loc[1]


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    PAIRS = [list(line.split("\n")) for line in DATA.split("\n\n")]

    print(parse(PAIRS))
    print(full_sort(PAIRS))
