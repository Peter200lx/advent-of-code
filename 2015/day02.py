import itertools
from pathlib import Path
from typing import List


def calc_needed_paper(dimen: List[int]) -> int:
    # Calculation required dimen to be pre-sorted
    assert len(dimen) > 2
    additional = dimen[0] * dimen[1]
    sides = itertools.combinations(dimen, 2)
    area = 2 * sum(x * y for x, y in sides)
    return area + additional


def calc_needed_ribbon(dimen: List[int]) -> int:
    # Calculation required dimen to be pre-sorted
    assert len(dimen) > 2
    length = 2 * (dimen[0] + dimen[1])
    bow = 1
    for x in dimen:
        bow *= x
    return length + bow


if __name__ == "__main__":
    DATA = Path("day02.input").read_text().strip()
    INPUT_DATA = [sorted(int(x) for x in sub.split("x")) for sub in DATA.split()]

    print(calc_needed_paper([2, 3, 4]))
    print(sum(calc_needed_paper(l) for l in INPUT_DATA))
    print(sum(calc_needed_ribbon(l) for l in INPUT_DATA))
