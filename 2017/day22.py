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
g_inf_count_p1 = 0
g_inf_count_p2 = 0


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


def run_burst_p1(grid: Dict[Tuple, str], start_dir: Tuple[int, int], start_loc: Tuple[int, int]) -> Tuple[Tuple, Tuple]:
    global g_inf_count_p1
    if grid[start_loc] == 'i':
        new_dir = MOVE_DICT['R'][start_dir]
        grid[start_loc] = 'c'
    else:
        new_dir = MOVE_DICT['L'][start_dir]
        grid[start_loc] = 'i'
        g_inf_count_p1 += 1
    return new_dir, (start_loc[0] + new_dir[0], start_loc[1] + new_dir[1])


def run_burst_p2(grid, start_dir: Tuple[int, int], start_loc: Tuple[int, int]):
    global g_inf_count_p2
    if grid[start_loc] == 'c':
        new_dir = MOVE_DICT['L'][start_dir]
        grid[start_loc] = 'w'
    elif grid[start_loc] == 'w':
        new_dir = start_dir
        grid[start_loc] = 'i'
        g_inf_count_p2 += 1
    elif grid[start_loc] == 'i':
        new_dir = MOVE_DICT['R'][start_dir]
        grid[start_loc] = 'f'
    elif grid[start_loc] == 'f':
        new_dir = MOVE_DICT['REV'][start_dir]
        grid[start_loc] = 'c'
    else:
        raise Exception(f"Unexpected board state grid[{start_loc}] == {grid[start_loct]}")
    return new_dir, (start_loc[0] + new_dir[0], start_loc[1] + new_dir[1])


if __name__ == '__main__':
    seed_grid = initialize_grid(DATA)
    board_dict = make_dict_grid(seed_grid)
    current_dir, current_loc = FACE_DICT['N'], (0, 0)
    for num_bursts in range(10000):
        current_dir, current_loc = run_burst_p1(board_dict, current_dir, current_loc)
    print(g_inf_count_p1)
    board_dict = make_dict_grid(seed_grid)
    current_dir, current_loc = FACE_DICT['N'], (0, 0)
    for num_bursts in range(10000000):
        current_dir, current_loc = run_burst_p2(board_dict, current_dir, current_loc)
    print(g_inf_count_p2)
