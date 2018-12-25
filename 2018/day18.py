from collections import defaultdict, namedtuple
from typing import List

import numpy as np

DATA = """
..|..|.|.|.||..#.#|...|..#.|.........|.......|..#.
#.|.........|||....#....|....##||.....|.|.........
..||......#.#||#.#.......#..#.#.###...|.#..#...#..
|....#....|.##.##.....##...##|..|....|..|#||...###
#|...|.#|..|......#.##....#|....|...|#......|.#|.|
..|....##.##.#..||##...#..##|......|...|#.||.#.#..
.#...#||...........#|.....|##....#.#...|#.|###..|.
||....#.#.|...||...###|.|#.....#.|#.|#...#.#.|...#
...#.....||.......#....#|###|####..|#|.###..||.#.#
|#|...||..##.||.||..#.#.|..#...#..|........#..|#..
#....||.|.....|.|.#|.##.|..|.#.....|..|.....#|.|..
|..||#........|#.|..|.|...#..#....#.|.....||#.#...
..|...||.|##||##..|...#|.....|#.|....#....||#.##..
#|..#|..||...|..|.|#|..##.#.......#|#....#||...#..
|#|.|...|..##...|.#||#..#...#....||.#.|...##..|..#
|..||.#.#..|....#...#.#..#..#...||.|.#.#.#.....#|.
.|##.####..||.#.|#.###....#...#.|..#.#.##.|..##..#
#|.......#......|.#..|.....||.|.#||#.#.##.#|....|.
.|..#.|#.##|....#......|.#||..|#..##.|..#......###
..###....#.||.#..|##.##..#|.#...|#|...#.|.|...#|#.
........||......|##||##..###|..|.##.#..#|##...|..#
.#....|....|...##.#.||##.....#|...|#.#||...#.....|
#...#|...###.|.|..|..#.|###.|.#.|.####|...|.#..|#.
...#..|.....|.#.##.|.#.#..|..##.##.#..|...#...|#..
..###.#|##|#.#.......|.|...||###|.#.........#..|..
..|#...||.#.#..|...|..#||...|.#.#......#...|..#...
.||..........|.#....|.||...|#.|.|||..||........|#.
#.##.#||..|.|#...|..#|.|#......|.||.......|...|#..
#.||.||#...#|||.....|.|.|.|...||.#..#.#.#|..|||.|.
.#...#...||||#...##.#.#......#|......#.|.....|#||.
.#|.###|#||.|#...#.|..|.|#.|#..#..#...|.|.|...|.|.
..#|.|#|..##|.||.|.....|#...#..|.|#....|.|..|..|#.
#....|..#.#.......#||..#....|.|..#.#|..#...|#.#.|.
#.#.|..|...#|.###||.#.....#|#|#.##..|.|#|....|....
....|#.#.||..|..#...|...|..|...|..#..#......#|.#..
..#..#|.|.|#.#.|.|.#.#.....#..|..#..|.......||#|#.
#|......|#..|.#...##|....|..|#||..|..||...||.#....
#..|#.......||.....|.||||#.|#.|....#|#....|#.#....
#.##.#.#..||......#...|......|#|...|.||.#.|..|....
####.|...||##|#|.......|||.#.#.....#...##.#|..#...
..|..|||..|.||#|#.|..#.|..#.|........###......#..|
..#|.....|||||#..||.....##..#...|||.....#......#.#
.#.|.||#.##.......||.#.||..#...|##..|.#.#...|...|.
.##........|..||.|.#|.|.||||..#...#..|..|#|#..|#|.
.#.#.....#|||..|...#.|...|...#.||..||###|.#|......
|.|#..#.#.|||||.#|.|......#.|#.||.....#..#...|#.|.
...|....#.###|.#.##......|#.##.....#.|.##.#......#
.#.#.....|..#.##..#|#|..#.#|##..##|..##.#..#....||
..#.#.|.....#.|..#.|.|#...|....#...|..|.|..#||...|
|.||.|...|...|##..||....|#.|..#..##....|#.#|##..|.""".strip()

EXAMPLE_DATA = """
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.""".strip()

OPEN = 0
WOOD = 1
YARD = 2

MAP_TYPE = {
    ".": OPEN,
    "|": WOOD,
    "#": YARD,
}

REV_MAP_TYPE = {v: k for k, v in MAP_TYPE.items()}

np.set_printoptions(
    linewidth=120, threshold=np.nan, formatter={"int": lambda x: REV_MAP_TYPE[x]}
)

Coord = namedtuple("Coord", ["y", "x"])

P2_NUM = 1_000_000_000
Seq = namedtuple("Seq", ["index", "value"])


def parse_input(input_str: str) -> np.ndarray:
    lines = input_str.split("\n")
    y_range = len(lines)
    x_range = len(lines[0])

    def from_input(y, x):
        return MAP_TYPE[lines[y][x]]
    from_input_vector = np.vectorize(from_input)
    return np.fromfunction(from_input_vector, (y_range, x_range), dtype=np.uint8)


def geo_tick(array: np.ndarray) -> None:
    reference_array = array.copy()
    for y, x in np.ndindex(reference_array.shape):
        loc = Coord(y, x)
        loc_type = reference_array[loc]
        surrounding = reference_array[max(loc.y - 1, 0):min(loc.y + 2, array.shape[1]),
                                      max(loc.x - 1, 0):min(loc.x + 2, array.shape[0])]
        if loc_type == OPEN:
            if (surrounding == WOOD).sum() >= 3:
                array[loc] = WOOD
        elif loc_type == WOOD:
            if (surrounding == YARD).sum() >= 3:
                array[loc] = YARD
        elif loc_type == YARD:
            if not ((surrounding == WOOD).sum() >= 1
                    and (surrounding == YARD).sum() >= 2):
                array[loc] = OPEN


def part_1(array: np.ndarray) -> int:
    for i in range(10):
        geo_tick(array)
    return (array == WOOD).sum() * (array == YARD).sum()


def part_2_build_array(array: np.ndarray) -> List[Seq]:
    seen_values = defaultdict(list)
    repeating_array = None
    distance = None
    for i in range(P2_NUM):
        geo_tick(array)
        value = (array == WOOD).sum() * (array == YARD).sum()
        if not distance:
            seen_values[value].append(i)
            if len(seen_values[value]) >= 3:
                my_locs = seen_values[value]
                delta_1 = my_locs[-1] - my_locs[-2]
                delta_2 = my_locs[-2] - my_locs[-3]
                if delta_1 == delta_2:
                    distance = delta_1
                    repeating_array = [Seq(i, value)]
        else:
            repeating_array.append(Seq(i, value))
            if len(repeating_array) == distance:
                break

    return repeating_array


def part_2(sequence: List[Seq], n: int) -> int:
    return sequence[(n - sequence[0].index - 1) % len(sequence)].value


if __name__ == '__main__':
    lumber_field = parse_input(DATA)
    print(part_1(lumber_field.copy()))

    repeating_sequence = part_2_build_array(lumber_field)
    print(part_2(repeating_sequence, P2_NUM))
