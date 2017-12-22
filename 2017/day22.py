from collections import defaultdict
from typing import List, Dict, Tuple, NamedTuple

DATA = """#.#.#.##.#.##.###.#.###.#
.#..#.....#..#######.##.#
......###..##..###..#...#
##....#.#.#....#..#..#..#
#..#....#.##.#.#..#..#.#.
..##..##.##..##...#...###
..#.#....#..####.##.##...
###...#.#...#.######...#.
..#####...###..#####.#.##
...#..#......####.##..#.#
#...##..#.#####...#.##...
..#.#.###.##.##....##.###
##.##...###....#######.#.
#.#...#.#..#.##..##..##.#
.#...###...#..#..####....
####...#...##.####..#.#..
......#.....##.#.##....##
###.......####..##.#.##..
....###.....##.##..###.#.
.##..##.#.###.###..#.###.
..#..##.######.##........
#..#.#..#.###....##.##..#
.##.#.#...######...##.##.
##..#..#..##.#.#..#..####
#######.#.######.#.....##"""
EXAMPLE_DATA = """..#
#..
..."""
FACE_DICT = {'N': (1, 0),
             'S': (-1, 0),
             'E': (0, 1),
             'W': (0, -1)}
MOVE_DICT = {'L': {FACE_DICT['N']: FACE_DICT['W'],
                   FACE_DICT['S']: FACE_DICT['E'],
                   FACE_DICT['E']: FACE_DICT['N'],
                   FACE_DICT['W']: FACE_DICT['S']},
             'R': {FACE_DICT['N']: FACE_DICT['E'],
                   FACE_DICT['S']: FACE_DICT['W'],
                   FACE_DICT['E']: FACE_DICT['S'],
                   FACE_DICT['W']: FACE_DICT['N']},
             'REV': {FACE_DICT['N']: FACE_DICT['S'],
                     FACE_DICT['S']: FACE_DICT['N'],
                     FACE_DICT['E']: FACE_DICT['W'],
                     FACE_DICT['W']: FACE_DICT['E']}}
P1_DICT = {'c': 'i',
           'i': 'c'}
P2_DICT = {'c': 'w',
           'w': 'i',
           'i': 'f',
           'f': 'c'}
NEW_DIR = {'c': lambda x: MOVE_DICT['L'][x],
           'w': lambda x: x,
           'i': lambda x: MOVE_DICT['R'][x],
           'f': lambda x: MOVE_DICT['REV'][x]}


class Vector(NamedTuple):
    dir: Tuple[int, int]
    loc: Tuple[int, int]


def initialize_grid(input_str: str) -> List[List[str]]:
    ret_grid = []
    for line in input_str.split('\n'):
        ret_grid.append(['i' if i == '#' else 'c' for i in line])
    return ret_grid


def make_dict_grid(in_grid: List[List[str]]) -> Dict[Tuple[int, int], str]:
    ret_dict = defaultdict(lambda: 'c')
    center_y = len(in_grid) // 2
    for i, row in enumerate(in_grid):
        center_x = len(row) // 2
        for j, cell in enumerate(row):
            if cell:
                # Reversing y, keeping x the same for math style grid with 1,1 in the top-right quadrant
                ret_dict[(center_y - i, j - center_x)] = cell
    return ret_dict


def new_vect(new_dir: Tuple[int, int], old_loc: Tuple[int, int]) -> Vector:
    new_loc = new_dir[0] + old_loc[0], new_dir[1] + old_loc[1]
    return Vector(new_dir, new_loc)


def run_burst(grid: Dict[Tuple[int, int], str], start: Vector, evolve_dict: Dict[str, str]) -> Tuple[bool, Vector]:
    new_dir = NEW_DIR[grid[start.loc]](start.dir)
    grid[start.loc] = evolve_dict[grid[start.loc]]
    return grid[start.loc] == 'i', new_vect(new_dir, start.loc)


if __name__ == '__main__':
    seed_grid = initialize_grid(DATA)
    board_dict = make_dict_grid(seed_grid)
    current_vec = Vector(FACE_DICT['N'], (0, 0))
    count = 0
    for num_bursts in range(10000):
        new_inf, current_vec = run_burst(board_dict, current_vec, P1_DICT)
        if new_inf:
            count += 1
    print(count)
    board_dict = make_dict_grid(seed_grid)
    current_vec = Vector(FACE_DICT['N'], (0, 0))
    count = 0
    for num_bursts in range(10000000):
        new_inf, current_vec = run_burst(board_dict, current_vec, P2_DICT)
        if new_inf:
            count += 1
    print(count)
