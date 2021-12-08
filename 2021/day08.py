from pathlib import Path
from typing import List, FrozenSet, Dict

INPUT_FILE = Path(__file__).with_suffix(".input")

"""
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
"""

KNOWN_NUMS = {
    2: 1,
    3: 7,
    4: 4,
    7: 8,
}


def decode_line(left: List[str], right: List[str]) -> int:
    int_set_map: Dict[int, FrozenSet] = {}
    for seq in left:
        if len(seq) in KNOWN_NUMS:
            int_set_map[KNOWN_NUMS[len(seq)]] = frozenset(seq)
    n2_3_5_sets = {frozenset(seq) for seq in left if len(seq) == 5}
    n0_6_9_sets = {frozenset(seq) for seq in left if len(seq) == 6}
    for seq in n2_3_5_sets:
        if len(int_set_map[1] & seq) == 2:
            int_set_map[3] = seq
    for seq in n2_3_5_sets - {int_set_map[3]}:
        if len(int_set_map[4] | seq) == 7:
            int_set_map[2] = seq
    int_set_map[5] = next(iter(n2_3_5_sets - {int_set_map[3], int_set_map[2]}))
    for seq in n0_6_9_sets:
        if len(int_set_map[3] | seq) == len(seq):
            int_set_map[9] = seq
    for seq in n0_6_9_sets - {int_set_map[9]}:
        if len(int_set_map[1] & seq) == 2:
            int_set_map[0] = seq
    int_set_map[6] = next(iter(n0_6_9_sets - {int_set_map[9], int_set_map[0]}))
    set_to_num = {s: f"{n}" for n, s in int_set_map.items()}

    return int("".join(set_to_num[frozenset(seq)] for seq in right))


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    SEGMENTS = [
        (left.split(), right.split())
        for line in DATA.split("\n")
        for left, right in [line.split(" | ")]
    ]
    print(sum(len(seq) in KNOWN_NUMS for line in SEGMENTS for seq in line[1]))
    print(sum(decode_line(*line) for line in SEGMENTS))
