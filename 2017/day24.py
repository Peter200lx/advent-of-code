from collections import defaultdict
from copy import copy
from typing import List, Tuple, Set, Dict

DATA = """50/41
19/43
17/50
32/32
22/44
9/39
49/49
50/39
49/10
37/28
33/44
14/14
14/40
8/40
10/25
38/26
23/6
4/16
49/25
6/39
0/50
19/36
37/37
42/26
17/0
24/4
0/36
6/9
41/3
13/3
49/21
19/34
16/46
22/33
11/6
22/26
16/40
27/21
31/46
13/2
24/7
37/45
49/2
32/11
3/10
32/49
36/21
47/47
43/43
27/19
14/22
13/43
29/0
33/36
2/6"""
EXAMPLE_DATA = """0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10"""


def load_pieces(input_str: str) -> Set[Tuple[int, int]]:
    ret_list = set()
    for line in input_str.split("\n"):
        ret_list.add(tuple(int(i) for i in line.split("/")))
    # ret_list.sort(key=sum, reverse=True)
    return ret_list


def calc_strength(bridge_list: List[Tuple[int, int]]) -> int:
    return sum(sum(p) for p in bridge_list)


def gen_matching(
    prev_con: int, remaining: Set[Tuple[int, int]], cached_mapping: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
):
    if not cached_mapping:  # remaining must contain all possible items first run otherwise cache will be bad
        for part in remaining:
            cached_mapping[part[0]].append(part)
            if part[0] == part[1]:
                continue
            cached_mapping[part[1]].append(part)
    for part in cached_mapping[prev_con]:
        if part in remaining:
            yield part


def build_bridges(
    prev_piece: int,
    so_far: List[Tuple[int, int]],
    remaining: Set[Tuple[int, int]],
    part1: List[List[Tuple[int, int]]],
    part2: List[List[Tuple[int, int]]],
):
    leaf = True
    for possible_next in gen_matching(prev_piece, remaining):
        leaf = False
        new_bridge = copy(so_far)
        reduced = copy(remaining)
        reduced.remove(possible_next)
        next_piece = possible_next[0]
        if next_piece == prev_piece:
            next_piece = possible_next[1]
        new_bridge.append(possible_next)
        build_bridges(next_piece, new_bridge, reduced, part1, part2)

    if leaf:
        if calc_strength(so_far) > calc_strength(part1[0]):
            part1[:] = [so_far]

        if len(so_far) > len(part2[0]):
            part2[:] = [so_far]
        elif len(so_far) == len(part2[0]):
            if calc_strength(so_far) > calc_strength(part2[0]):
                part2[:] = [so_far]


if __name__ == "__main__":
    piece_list = load_pieces(DATA)
    print(piece_list)
    completed_bridges_p1 = [[]]
    completed_bridges_p2 = [[]]
    build_bridges(0, [], piece_list, completed_bridges_p1, completed_bridges_p2)
    print(completed_bridges_p1)
    print(calc_strength(completed_bridges_p1[0]))
    print(completed_bridges_p2)
    print(calc_strength(completed_bridges_p2[0]))
