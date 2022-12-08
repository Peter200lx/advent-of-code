from pathlib import Path
from typing import List, Tuple, Set, Dict

INPUT_FILE = Path(__file__).with_suffix(".input")


def solve(grid: List[List[int]]) -> int:
    seen_trees: Set[Tuple[int, int]] = set()
    for y, line in enumerate(grid):
        l_height = -1
        for x, height in enumerate(line):
            if height > l_height:
                seen_trees.add((x, y))
                l_height = height
        r_height = -1
        for x, height in reversed(list(enumerate(line))):
            if height > r_height:
                seen_trees.add((x, y))
                r_height = height
    for x in range(len(grid[0])):
        u_height = d_height = -1
        for y in range(len(grid)):
            if grid[y][x] > d_height:
                seen_trees.add((x, y))
                d_height = grid[y][x]
            if grid[len(grid) - y - 1][x] > u_height:
                seen_trees.add((x, len(grid) - y - 1))
                u_height = grid[len(grid) - y - 1][x]
    return len(seen_trees)


def tree_score(trees: Dict[Tuple[int, int], int], start_x: int, start_y: int) -> int:
    score = 1
    my_height = trees.get((start_x, start_y))

    seen_trees = 0
    for i in range(1, 999):
        tree_up = trees.get((start_x + i, start_y), 999)
        if tree_up < my_height:
            seen_trees += 1
        else:
            if tree_up != 999:
                seen_trees += 1
            break

    score *= seen_trees
    seen_trees = 0
    for i in range(1, 999):
        tree_down = trees.get((start_x - i, start_y), 999)
        if tree_down < my_height:
            seen_trees += 1
        else:
            if tree_down != 999:
                seen_trees += 1
            break

    score *= seen_trees
    seen_trees = 0
    for i in range(1, 999):
        tree_left = trees.get((start_x, start_y - i), 999)
        if tree_left < my_height:
            seen_trees += 1
        else:
            if tree_left != 999:
                seen_trees += 1
            break

    score *= seen_trees
    seen_trees = 0
    for i in range(1, 999):
        tree_right = trees.get((start_x, start_y + i), 999)
        if tree_right < my_height:
            seen_trees += 1
        else:
            if tree_right != 999:
                seen_trees += 1
            break

    score *= seen_trees
    return score


def top_scenic(grid: List[List[int]]) -> int:
    tree_point_cloud = {}
    for y, line in enumerate(grid):
        for x, height in enumerate(line):
            tree_point_cloud[(x, y)] = height
    best_score = 0
    for x in range(1, len(grid[0]) - 1):
        for y in range(1, len(grid) - 1):
            best_score = max(best_score, tree_score(tree_point_cloud, x, y))
    return best_score


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT_DATA = [[int(i) for i in line] for line in DATA.split("\n")]

    print(solve(INPUT_DATA))
    print(top_scenic(INPUT_DATA))
