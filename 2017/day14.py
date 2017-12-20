from typing import List

import numpy as np
from scipy.ndimage import label

from day10 import part_two, get_hash_str, SALT

DATA = "ljoxqyyw"
EXAMPLE_DATA = "flqrgnkx"


def build_array(seed: str) -> List[str]:
    rows = []
    for i in range(128):
        row_seed = [ord(i) for i in (seed + '-' + str(i))] + SALT
        knot_list = [i for i in range(256)]
        part_two(knot_list, row_seed)
        row_str = ''.join([f"{int(c, 16):04b}" for c in get_hash_str(knot_list)])
        int_list = [1 if c is '1' else 0 for c in row_str]
        rows.append(int_list)
    return rows


if __name__ == '__main__':
    disk = build_array(DATA)

    sum_bits = 0
    for row in disk:
        bin_sum = sum(row)
        print(f"sum {bin_sum} from {''.join(str(i) for i in row)}")
        sum_bits += bin_sum

    print(sum_bits)

    nparray = np.array(disk)
    print(nparray)
    labeled_array, count = label(nparray)
    print(labeled_array)
    print(count)
