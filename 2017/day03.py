from typing import Tuple
import operator

import numpy as np

np.set_printoptions(linewidth=100)

EXAMPLE_DATA = """23"""
DATA = """277678"""

N, S, E, W = (-1, 0), (1, 0), (0, 1), (0, -1)
LEFT = {N: W, S: E, E: N, W: S}

SURROUNDING = [(x, y) for x in range(-1, 2) for y in range(-1, 2) if not (x == 0 and y == 0)]


def wanted_size(maxval: int) -> int:
    odd_val = 1
    while maxval > odd_val * odd_val:
        odd_val += 2
    return odd_val


def construct_square(maxval: int) -> np.ndarray:
    size = wanted_size(maxval)
    grid = np.zeros((size, size), dtype=np.int64)
    initial = size // 2
    cur_loc = (initial, initial)
    next_val = 1
    direction = S
    while next_val <= maxval:
        grid[cur_loc] = next_val
        next_val += 1
        next_loc = tuple(map(operator.add, cur_loc, LEFT[direction]))
        if grid[next_loc] == 0:
            cur_loc = next_loc
            direction = LEFT[direction]
        else:
            cur_loc = tuple(map(operator.add, cur_loc, direction))

    return grid


def find_distance(grid: np.ndarray, value: int) -> int:
    x, y = np.where(grid == value)
    center = len(grid[0, :]) // 2
    return abs(y[0] - center) + abs(x[0] - center)


def sum_surrounding(grid: np.ndarray, location: Tuple[int, int]) -> int:
    # print(grid[location[0]-1:location[0]+2, location[1]-1:location[1]+2])
    sumval = 0
    for diff in SURROUNDING:
        this_location = tuple(map(operator.add, location, diff))
        sumval += grid[this_location]
    # print(sumval)
    return sumval


def construct_adv_square(maxval: int) -> int:
    size = 11
    grid = np.zeros((size, size), dtype=np.int64)
    initial = size // 2
    cur_loc = (initial, initial)
    cur_val = 1
    direction = S
    while cur_val <= maxval:
        cur_val = sum_surrounding(grid, cur_loc) or 1
        grid[cur_loc] = cur_val
        next_loc = tuple(map(operator.add, cur_loc, LEFT[direction]))
        if grid[next_loc] == 0:
            cur_loc = next_loc
            direction = LEFT[direction]
        else:
            cur_loc = tuple(map(operator.add, cur_loc, direction))

    print(grid)
    return cur_val


if __name__ == "__main__":
    START_SQUARE = int(DATA)
    GRID = construct_square(START_SQUARE)
    print(GRID)
    print(find_distance(GRID, START_SQUARE))
    print(construct_adv_square(START_SQUARE))
