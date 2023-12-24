from itertools import combinations
from pathlib import Path
from typing import List, Tuple

INPUT_FILE = Path(__file__).with_suffix(".input")

TEST_RANGE = range(7, 27)
P1_RANGE = range(200_000_000_000_000, 400_000_000_000_000)

TYPE_2D = Tuple[int, int]
TYPE_2D_LINE = Tuple[TYPE_2D, TYPE_2D]
TYPE_3D = Tuple[int, int, int]
TYPE_3D_LINE = Tuple[TYPE_3D, TYPE_3D]


def line_intersection(line1: TYPE_2D_LINE, line2: TYPE_2D_LINE) -> TYPE_2D:
    # From https://stackoverflow.com/a/20677983
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise ZeroDivisionError("lines do not intersect")

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    return x, y


def part_one(hailstones: List[TYPE_3D_LINE]) -> int:
    lines = [
        (tuple(p[:2]), tuple(v[:2]), tuple([i + j for i, j in zip(p[:2], v[:2])]))
        for p, v in hailstones
    ]
    count = 0
    for l1, l2 in combinations(lines, 2):
        try:
            inter = line_intersection(l1[::2], l2[::2])
        except ZeroDivisionError:
            continue
        # Make sure we're only considering points in the future
        backwards = False
        for l in (l1, l2):
            inter_d = (l[0][0] - inter[0], l[0][1] - inter[1])
            if any((v * i) > 0 for v, i in zip(l[1], inter_d)):
                backwards = True
                break
        if backwards:
            continue
        r = P1_RANGE  # TEST_RANGE if testing
        if r.start <= inter[0] <= r.stop and r.start <= inter[1] <= r.stop:
            count += 1
    return count


def part_two(hailstones: Tuple[TYPE_3D, TYPE_3D]) -> int:
    pass  # To solve tomorrow


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    HAILSTONES = [
        (tuple(map(int, p.split(", "))), tuple(map(int, v.split(", "))))
        for line in DATA.split("\n")
        for p, v in [line.split(" @ ")]
    ]

    print(part_one(HAILSTONES))
    print(part_two(HAILSTONES))
