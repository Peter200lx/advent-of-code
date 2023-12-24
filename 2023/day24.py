from itertools import combinations
from pathlib import Path
from typing import Iterable, List, Optional, Union, Tuple

INPUT_FILE = Path(__file__).with_suffix(".input")

TEST_RANGE = range(7, 27)
P1_RANGE = range(200_000_000_000_000, 400_000_000_000_000)

TYPE_2D = Tuple[int, int]
TYPE_2D_LINE = Tuple[TYPE_2D, TYPE_2D]
TYPE_3D = Tuple[int, int, int]
TYPE_3D_LINE = Tuple[TYPE_3D, TYPE_3D]


def line_intersection(line1: TYPE_2D_LINE, line2: TYPE_2D_LINE) -> Optional[TYPE_2D]:
    # From https://stackoverflow.com/a/20677983
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    return int(x), int(y)


def part_one(hailstones: List[TYPE_3D_LINE]) -> int:
    lines = [
        (tuple(p[:2]), tuple(v[:2]), tuple(i + j for i, j in zip(p[:2], v[:2])))
        for p, v in hailstones
    ]
    count = 0
    for l1, l2 in combinations(lines, 2):
        inter = line_intersection(l1[::2], l2[::2])  # point 1, not vector, point 2
        if inter is None:
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


def fast_fail_p1(
    hailstones: List[TYPE_3D_LINE], rock_delta: Union[TYPE_2D, TYPE_3D], proj: range
) -> Optional[TYPE_2D]:
    master_inter = None
    for l1, l2 in combinations(hailstones, 2):
        l1_p1: TYPE_2D = tuple(l1[0][i] for i in proj)
        l2_p1: TYPE_2D = tuple(l2[0][i] for i in proj)
        l1_p2: TYPE_2D = tuple(l1[0][i] + l1[1][i] + rock_delta[i] for i in proj)
        l2_p2: TYPE_2D = tuple(l2[0][i] + l2[1][i] + rock_delta[i] for i in proj)

        inter = line_intersection((l1_p1, l1_p2), (l2_p1, l2_p2))
        if inter is None:
            return
        if master_inter is None:
            master_inter = inter
        elif inter != master_inter:
            return
    return master_inter


def vec_2d_gen() -> Iterable[TYPE_2D]:
    for x in range(999999):
        for y in range(x + 1):
            yield x, y
            yield x, -y
            yield -x, y
            yield -x, -y


def vec_1d_gen() -> Iterable[int]:
    for z in range(999999):
        yield z
        yield -z


def part_two(hailstones: List[TYPE_3D_LINE]) -> int:
    # Using the idea from reddit of using the 2d crossings after adjusting for rock vector
    # https://www.reddit.com/r/adventofcode/comments/18pptor/comment/kepufsi/
    for rock_vel_2d in vec_2d_gen():
        inter_2d_xy = fast_fail_p1(hailstones[:10], rock_vel_2d, range(2))
        if inter_2d_xy:
            for z in vec_1d_gen():
                inter_2d_yz = fast_fail_p1(hailstones[:10], rock_vel_2d + (z,), range(1, 3))
                if inter_2d_yz:
                    assert inter_2d_xy[1] == inter_2d_yz[0]
                    return sum(inter_2d_xy) + inter_2d_yz[1]


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    HAILSTONES = [
        (tuple(map(int, p.split(", "))), tuple(map(int, v.split(", "))))
        for line in DATA.split("\n")
        for p, v in [line.split(" @ ")]
    ]

    print(part_one(HAILSTONES))
    print(part_two(HAILSTONES))
