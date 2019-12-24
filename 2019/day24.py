from copy import deepcopy
from typing import NamedTuple, Dict

import numpy as np

DATA = """
.##..
##.#.
##.##
.#..#
#.###""".strip()

EXAMPLE_DATA = """
....#
#..#.
#..##
..#..
#....""".strip()

OPEN = 0
BUG = 1

MAP_TYPE = {".": OPEN, "#": BUG}

REV_MAP_TYPE = {v: k for k, v in MAP_TYPE.items()}

np.set_printoptions(formatter={"int": lambda x: REV_MAP_TYPE[x]})


class Point(NamedTuple):
    y: int
    x: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.y + other.y, self.x + other.x)


ADJACENT = (Point(-1, 0), Point(1, 0), Point(0, 1), Point(0, -1))


def parse_input(input_str: str) -> np.ndarray:
    lines = input_str.split("\n")
    y_range = len(lines)
    x_range = len(lines[0])

    def from_input(y, x):
        return MAP_TYPE[lines[y][x]]

    from_input_vector = np.vectorize(from_input)
    return np.fromfunction(from_input_vector, (y_range, x_range), dtype=np.uint8)


def adjacent_values(array: np.ndarray, loc: Point):
    for direction in ADJACENT:
        move = loc + direction
        if 0 <= move.y < array.shape[1] and 0 <= move.x < array.shape[0]:
            yield array[move]


def minute_passes(array: np.ndarray) -> None:
    reference_array: np.ndarray = array.copy()
    for y, x in np.ndindex(reference_array.shape):
        loc = Point(y, x)
        loc_type = reference_array[loc]
        bug_count = sum(adjacent_values(reference_array, loc))
        if loc_type == BUG:
            if bug_count != 1:
                array[loc] = OPEN
        if loc_type == OPEN:
            if bug_count in (1, 2):
                array[loc] = BUG


def calc_biodiversity(array: np.ndarray) -> int:
    power = 0
    bio = 0
    for x in np.nditer(array):
        if x == BUG:
            bio += 2 ** power
        power += 1
    return bio


def part_1(array: np.ndarray) -> int:
    previous_fields = {array.tobytes()}
    while True:
        minute_passes(array)
        array_hash = array.tobytes()
        if array_hash in previous_fields:
            return calc_biodiversity(array)
        else:
            previous_fields.add(array_hash)


def recursive_adjacent_values(
    array_dict: Dict[int, np.ndarray], level: int, loc: Point
):
    for direction in ADJACENT:
        move = (loc.y + direction.y, loc.x + direction.x)
        if move == (2, 2):
            if level + 1 in array_dict:
                inside_array = array_dict[level + 1]
                if loc == (1, 2):
                    yield from inside_array[0, :]
                elif loc == (3, 2):
                    yield from inside_array[4, :]
                elif loc == (2, 1):
                    yield from inside_array[:, 0]
                elif loc == (2, 3):
                    yield from inside_array[:, 4]
            else:
                yield OPEN
        elif 0 <= move[0] < 5 and 0 <= move[1] < 5:
            if level in array_dict:
                yield array_dict[level][move]
            else:
                yield OPEN
        else:
            if level - 1 in array_dict:
                outside_array = array_dict[level - 1]
                if move[0] < 0:
                    yield outside_array[(1, 2)]
                elif move[0] >= 5:
                    yield outside_array[(3, 2)]
                elif move[1] < 0:
                    yield outside_array[(2, 1)]
                elif move[1] >= 5:
                    yield outside_array[(2, 3)]
            else:
                yield OPEN


def minute_passes_recursive(array_dict: Dict[int, np.ndarray]) -> None:
    reference_array_dict = deepcopy(array_dict)
    below = min(array_dict.keys()) - 1
    above = max(array_dict.keys()) + 1
    array_dict[below] = np.zeros(array_dict[0].shape, dtype=np.uint8)
    array_dict[above] = np.zeros(array_dict[0].shape, dtype=np.uint8)
    for level in sorted(array_dict.keys()):
        for y, x in np.ndindex(array_dict[level].shape):
            if 2 == y == x:
                continue
            loc = Point(y, x)
            loc_type = (
                reference_array_dict[level][loc]
                if level in reference_array_dict
                else OPEN
            )
            bug_count = sum(recursive_adjacent_values(reference_array_dict, level, loc))
            if loc_type == BUG:
                if bug_count != 1:
                    array_dict[level][loc] = OPEN
            if loc_type == OPEN:
                if bug_count in (1, 2):
                    array_dict[level][loc] = BUG
    if array_dict[below].sum() == 0:
        del array_dict[below]
    if array_dict[above].sum() == 0:
        del array_dict[above]


def part_2(array: np.ndarray, runtime=200) -> int:
    infinite_fields = {0: array}
    for i in range(runtime):
        minute_passes_recursive(infinite_fields)
    bug_count = 0
    # for level in sorted(infinite_fields.keys()):
    #     print(f"Depth {level}:")
    #     print(infinite_fields[level])
    for level, field in infinite_fields.items():
        bug_count += (field == BUG).sum()
    return bug_count


if __name__ == "__main__":
    scan_field = parse_input(DATA)

    print(part_1(scan_field.copy()))
    print(part_2(scan_field))
