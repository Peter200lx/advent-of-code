import math
from pathlib import Path

FILE_DIR = Path(__file__).parent


def read_map(lines):
    tree_pos = set()
    y_max = len(lines)
    x_max = len(lines[0])
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            x_max = max(x_max, x)
            if c == "#":
                tree_pos.add((x, y))
    return x_max, y_max, tree_pos


def move_check(width, end_y, tree_pos, slope=(3, 1)):
    loc = (0, 0)
    count = 0
    while loc[1] <= end_y:
        tree_x = loc[0] % width
        if (tree_x, loc[1]) in tree_pos:
            count += 1
        loc = loc[0] + slope[0], loc[1] + slope[1]
    return count


def check_all(width, end_y, tree_pos):
    counts = [move_check(width, end_y, tree_pos, slope) for slope in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))]
    return math.prod(counts)


if __name__ == "__main__":
    DATA = (FILE_DIR / "day03.input").read_text().strip()
    repeat_width, end_height, trees = read_map(DATA.split("\n"))
    print(move_check(repeat_width, end_height, trees))
    print(check_all(repeat_width, end_height, trees))
