import numpy as np

DATA = """7803"""
DATA = int(DATA)

GRID_SIZE = (300, 300)


def power_wrapper(serial_number):
    def power(ix, iy):
        rack_id = ix + 10
        power_level = rack_id * iy
        val = (power_level + serial_number) * rack_id
        h_digit = val // 10**2 % 10
        return h_digit - 5

    return power


def find_max(grid, square=3):
    max_seg = (0, 0, 0)  # x, y, sum
    for ix, iy in np.ndindex((GRID_SIZE[0] - square, GRID_SIZE[1] - square)):
        local_sum = grid[ix: ix + square, iy: iy + square].sum()
        if local_sum > max_seg[2]:
            max_seg = (ix, iy, local_sum)
    return max_seg


def find_all_sizes(grid):
    max_any = (0, 0, 0, 0)  # x, y, square, sum
    for i in range(GRID_SIZE[0]):
        size_max = find_max(grid, square=i)
        if size_max[2] > max_any[3]:
            max_any = size_max[0], size_max[1], i, size_max[2]
            # print(max_any)
        if i > max_any[2] + 10:  # Guess that past some limit we won't find more
            # print(f"Last square tested is {i}x{i}")
            break
    return max_any


if __name__ == '__main__':
    calc_power_vector = np.vectorize(power_wrapper(DATA))
    fuel_cells = np.fromfunction(calc_power_vector, GRID_SIZE, dtype=np.int16)
    # print(fuel_cells)
    print(find_max(fuel_cells))
    print(find_all_sizes(fuel_cells))
