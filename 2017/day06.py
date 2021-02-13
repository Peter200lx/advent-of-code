from typing import List, Tuple

EXAMPLE_DATA = """0 2   7   0"""
DATA = """4	10	4	1	8	4	9	14	5	1	14	15	0	15	3	5"""


def distribute_from_index(buckets: list[int], index: int):
    pool = buckets[index]
    buckets[index] = 0
    while pool:
        index += 1
        index %= len(buckets)
        buckets[index] += 1
        pool -= 1


def cycle_calc(starting_banks: List[int]) -> Tuple[int, int]:
    banks = starting_banks.copy()
    seen = {}

    count = 0
    while tuple(banks) not in seen:
        seen[tuple(banks)] = count
        distribute_from_index(banks, banks.index(max(banks)))
        count += 1

    return count, count - seen[tuple(banks)]


if __name__ == "__main__":
    BANKS = [int(i) for i in DATA.split()]
    for part in cycle_calc(BANKS):
        print(part)
