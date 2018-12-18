from collections import defaultdict, namedtuple

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
    linewidth=500, threshold=np.nan, formatter={"int": lambda x: REV_MAP_TYPE[x]}
)

Coord = namedtuple("Coord", ["y", "x"])
Range = namedtuple("Range", ["y_max", "x_max"])

P2_NUM = 1_000_000_000
Seq = namedtuple("Seq", ["index", "value"])


def parse_input(input_str):
    lines = input_str.split("\n")
    y_range = len(lines)
    x_range = len(lines[0])

    def from_input(y, x):
        return MAP_TYPE[lines[y][x]]
    from_input_vector = np.vectorize(from_input)
    return np.fromfunction(from_input_vector, (y_range, x_range), dtype=np.int16), Range(y_range, x_range)


def get_surrounding(array, a_range, loc):
    surrounding = []
    for y in range(max(loc.y - 1, 0), min(loc.y + 2, a_range.y_max)):
        for x in range(max(loc.x - 1, 0), min(loc.x + 2, a_range.y_max)):
            if (y, x) == loc:
                continue
            surrounding.append(array[y, x])
    return surrounding


def geo_tick(array, a_range):
    reference_array = array.copy()
    for y, x in np.ndindex(reference_array.shape):
        loc = Coord(y, x)
        loc_type = array[loc]
        surrounding = get_surrounding(reference_array, a_range, loc)
        if loc_type == OPEN:
            if len([s for s in surrounding if s == WOOD]) >= 3:
                array[loc] = WOOD
        elif loc_type == WOOD:
            if len([s for s in surrounding if s == YARD]) >= 3:
                array[loc] = YARD
        elif loc_type == YARD:
            if not (len([s for s in surrounding if s == WOOD]) >= 1
                    and len([s for s in surrounding if s == YARD]) >= 1):
                array[loc] = OPEN


def part_1(array, a_range):
    for i in range(10):
        geo_tick(array, a_range)
    return (array == WOOD).sum() * (array == YARD).sum()


def part_2_build_array(array, a_range):
    seen_values = defaultdict(list)
    repeating_array = None
    distance = None
    for i in range(P2_NUM):
        geo_tick(array, a_range)
        value = (array == WOOD).sum() * (array == YARD).sum()
        if not distance:
            seen_values[value].append(i)
            if len(seen_values[value]) > 4:
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


def part_2(sequence, n):
    return sequence[(n - sequence[0].index - 1) % len(sequence)].value


if __name__ == '__main__':
    lumber_field, field_range = parse_input(DATA)
    print(part_1(lumber_field.copy(), field_range))

    repeating_sequence = part_2_build_array(lumber_field, field_range)
    print(part_2(repeating_sequence, P2_NUM))
