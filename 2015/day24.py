import sys
from functools import reduce
from itertools import combinations
from operator import mul
from typing import Tuple, Set

DATA = """1
2
3
7
11
13
17
19
23
31
37
41
43
47
53
59
61
67
71
73
79
83
89
97
101
103
107
109
113"""


def balance_total(remaining_packages: Set[int], balance_sum: int) -> bool:
    total = sum(remaining_packages)
    if total == balance_sum:
        return True
    elif total < balance_sum:
        return False
    for size in range(2, len(remaining_packages) - 1):
        for side in combinations(remaining_packages, size):
            if sum(side) == balance_sum:
                if balance_total(set(remaining_packages) - set(side), balance_sum):
                    return True
    return False


def generate_even_mix(all_packages: Tuple[int], bucket_count: int = 3) -> int:
    package_sums = sum(all_packages)
    assert package_sums % bucket_count == 0, "Package sum must be evenly divisible by bucket_count"
    per_bucket_target = package_sums // bucket_count
    min_balanced: int = sys.maxsize
    for size in range(2, len(all_packages)):
        for main in combinations(all_packages, size):
            if sum(main) != per_bucket_target:
                continue
            if balance_total(set(all_packages) - set(main), per_bucket_target):
                min_balanced = min(min_balanced, reduce(mul, main, 1))
        if min_balanced != sys.maxsize:
            return min_balanced


if __name__ == "__main__":
    PACKAGES = tuple(int(line) for line in DATA.split("\n"))
    print(generate_even_mix(PACKAGES))

    print(generate_even_mix(PACKAGES, bucket_count=4))
