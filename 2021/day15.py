import heapq
from pathlib import Path
from typing import List

INPUT_FILE = Path(__file__).with_suffix(".input")


def p2_find_value(grid: List[List[int]], x: int, y: int) -> int:
    size_x, size_y = len(grid[-1]), len(grid)
    raw_value = grid[y % size_y][x % size_x]
    raw_value += x // size_x + y // size_y
    return raw_value - 9 if raw_value > 9 else raw_value


def find_paths_from_start(grid: List[List[int]], p2: bool = False) -> int:
    heap = []
    heapq.heappush(heap, (0, (0, 0)))
    coord_cost = {}
    finish = (len(grid[-1]) - 1, len(grid) - 1)
    get_func = lambda g, x, y: g[y][x]
    if p2:
        get_func = p2_find_value
        finish = (len(grid[-1]) * 5 - 1, len(grid) * 5 - 1)
    while heap:
        risk_so_far, cur_coord = heapq.heappop(heap)
        if coord_cost.get(cur_coord, 999999999) <= risk_so_far:
            continue
        if cur_coord == finish:
            return risk_so_far
        coord_cost[cur_coord] = risk_so_far
        for diff_x, diff_y in ((-1, 0), (0, -1), (0, 1), (1, 0)):
            new_x, new_y = cur_coord[0] + diff_x, cur_coord[1] + diff_y
            if 0 <= new_x <= finish[0] and 0 <= new_y <= finish[1]:
                other_risk = risk_so_far + get_func(grid, new_x, new_y)
                if coord_cost.get((new_x, new_y), 999999999) <= other_risk:
                    continue
                heapq.heappush(heap, (other_risk, (new_x, new_y)))


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    GRID = [[int(n) for n in line] for line in DATA.split("\n")]
    print(find_paths_from_start(GRID))
    print(find_paths_from_start(GRID, p2=True))
