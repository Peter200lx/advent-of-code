from itertools import combinations
from pathlib import Path
from typing import NamedTuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int


def p1(field: list[Coord]) -> int:
    return max(
        (abs(first.x - second.x) + 1) * (abs(first.y - second.y) + 1)
        for first, second in combinations(field, 2)
    )


def check_lines(first: Coord, second: Coord, lines: list[tuple]) -> bool:
    min_x, max_x = sorted((first.x, second.x))
    min_y, max_y = sorted((first.y, second.y))
    for line in lines:
        if isinstance(line[0], int):  # Vertical line
            if min_x < line[0] < max_x and (
                line[1][0] <= min_y < line[1][1] or line[1][0] < max_y <= line[1][1]
            ):
                return False
        else:  # Horizontal line
            if min_y < line[1] < max_y and (
                line[0][0] <= min_x < line[0][1] or line[0][0] < max_x <= line[0][1]
            ):
                return False
    return True


def p2(field: list[Coord]) -> int:
    lines = []
    prev_point = field[-1]
    for point in field:
        if prev_point.x == point.x:
            lines.append((point.x, tuple(sorted((point.y, prev_point.y)))))
        elif prev_point.y == point.y:
            lines.append((tuple(sorted((point.x, prev_point.x))), point.y))
        prev_point = point
    return max(
        (abs(first.x - second.x) + 1) * (abs(first.y - second.y) + 1)
        for first, second in combinations(field, 2)
        if check_lines(first, second, lines)
    )


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    FIELD = [
        Coord(int(x), int(y)) for line in DATA.split("\n") for x, y in [line.split(",")]
    ]

    print(p1(FIELD))
    print(p2(FIELD))
