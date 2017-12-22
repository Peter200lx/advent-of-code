from collections import defaultdict
from typing import List, Dict, Tuple

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


def initialize_grid(input_str: str) -> List[List[str]]:
    ret_grid = []
    for line in input_str.split('\n'):
        ret_grid.append(['i' if i == '#' else 'c' for i in line])
    return ret_grid


def make_dict_grid(in_grid: List[List[str]]) -> Dict[Tuple, str]:
    ret_dict = defaultdict(lambda: 'c')
    center_y = len(in_grid) // 2
    for i, row in enumerate(in_grid):
        center_x = len(row) // 2
        for j, cell in enumerate(row):
            if cell:
                # Reversing y, keeping x the same for math style grid with 1,1 in the top-right quadrant
                ret_dict[(center_y - i, j - center_x)] = cell
    return ret_dict


def run_burst(grid, start_dir: Tuple[int, int], start_loc: Tuple[int, int], evolve_dict: Dict[str, str]):
    infected = False
    cur_val = grid[start_loc]
    grid[start_loc] = evolve_dict[cur_val]
    if grid[start_loc] == 'i':
        infected = True
    if cur_val == 'c':
        new_dir = MOVE_DICT['L'][start_dir]
    elif cur_val == 'w':
        new_dir = start_dir
    elif cur_val == 'i':
        new_dir = MOVE_DICT['R'][start_dir]
    elif cur_val == 'f':
        new_dir = MOVE_DICT['REV'][start_dir]
    else:
        raise Exception(f"Unexpected board state grid[{start_loc}] == {grid[start_loct]}")
    return infected, new_dir, (start_loc[0] + new_dir[0], start_loc[1] + new_dir[1])


if __name__ == '__main__':
    seed_grid = initialize_grid(DATA)
    board_dict = make_dict_grid(seed_grid)
    current_dir, current_loc = FACE_DICT['N'], (0, 0)
    count = 0
    for num_bursts in range(10000):
        new_inf, current_dir, current_loc = run_burst(board_dict, current_dir, current_loc, P1_DICT)
        if new_inf:
            count += 1
    print(count)
    board_dict = make_dict_grid(seed_grid)
    current_dir, current_loc = FACE_DICT['N'], (0, 0)
    count = 0
    for num_bursts in range(10000000):
        new_inf, current_dir, current_loc = run_burst(board_dict, current_dir, current_loc, P2_DICT)
        if new_inf:
            count += 1
    print(count)
