import operator
from functools import reduce
from typing import List, Tuple, Optional

from math import sqrt

DATA = """14,58,0,116,179,16,1,104,2,254,167,86,255,55,122,244"""
EXAMPLE_DATA = """3, 4, 1, 5"""


def get_list_sequence(list_size: int, start_loc: int, range_size: int) -> Tuple[slice, Optional[slice]]:
    assert (start_loc < list_size) and (range_size <= list_size)
    if start_loc + range_size < list_size:
        return slice(start_loc, start_loc + range_size), None
    second_half = (start_loc + range_size) % list_size
    return slice(start_loc, list_size), slice(0, second_half)


def proc_inst(knots_l: List[int], inst: int, cur_loc: int, skip_size: int) -> Tuple[int, int]:
    list_size = len(knots_l)
    first, second = get_list_sequence(list_size, cur_loc, inst)
    if second is None:
        # print(f"1st range {first} 2nd range <> == {knots_l[first]}")
        knots_l[first] = reversed(knots_l[first])
    else:
        full_sub_list = knots_l[first] + knots_l[second]
        # print(f"1st range {first} 2nd range {second} == {full_sub_list}")
        full_sub_list.reverse()
        knots_l[first] = full_sub_list[:first.stop - first.start]
        knots_l[second] = full_sub_list[first.stop - first.start:]
    # print(knots_l)
    return ((cur_loc + inst + skip_size) % list_size), (skip_size + 1)


def part_one(knots_l: List[int], instructions: List[int]) -> List[int]:
    skip_size = 0
    current_location = 0
    for inst in instructions:
        current_location, skip_size = proc_inst(knots_l, inst, current_location, skip_size)
    return knots_l


INPUT_P1 = [int(i) for i in DATA.split(',')]
knot_list = [i for i in range(256)]

part_one(knot_list, INPUT_P1)
print(knot_list)
print(knot_list[0] * knot_list[1])


def part_two(knots_l: List[int], instructions: List[int]) -> List[int]:
    skip_size = 0
    current_location = 0
    for rounds in range(64):
        for inst in instructions:
            current_location, skip_size = proc_inst(knots_l, inst, current_location, skip_size)
    return knots_l


def get_hash_str(knots_l: List[int]) -> str:
    square_root = sqrt(len(knots_l))
    assert square_root.is_integer()
    square_root = int(square_root)
    ret_str = ""
    for i in range(square_root):
        sub_list = knots_l[i * square_root:(i + 1) * square_root]
        ret_str += f"{reduce(operator.xor, sub_list):02x}"
    return ret_str


INPUT_P2 = [ord(i) for i in DATA] + [17, 31, 73, 47, 23]

knot_list = [i for i in range(256)]

part_two(knot_list, INPUT_P2)
print(knot_list)
print(get_hash_str(knot_list))
