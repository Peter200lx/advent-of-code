import re
from pathlib import Path
from typing import NamedTuple, Set

INPUT_FILE = Path(__file__).with_suffix(".input")

RE_NUMS = re.compile(r"-?\d+")


class Pos(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other: "Pos") -> "Pos":
        return Pos(self.x + other.x, self.y + other.y, self.z + other.z)


DIRS = {
    Pos(-1, 0, 0),
    Pos(1, 0, 0),
    Pos(0, -1, 0),
    Pos(0, 1, 0),
    Pos(0, 0, -1),
    Pos(0, 0, 1),
}


def part_1(points: Set[Pos]) -> int:
    outside = 0
    for point in points:
        for direc in DIRS:
            if point + direc not in points:
                outside += 1
    return outside


def part_2(points: Set[Pos]) -> int:
    min_x, max_x = min(p.x for p in points) - 1, max(p.x for p in points) + 1
    min_y, max_y = min(p.y for p in points) - 1, max(p.y for p in points) + 1
    min_z, max_z = min(p.z for p in points) - 1, max(p.z for p in points) + 1
    visited_points: Set[Pos] = set()
    to_check = {Pos(min_x, min_y, min_z)}
    real_surface_count = 0
    while to_check:
        point = to_check.pop()
        visited_points.add(point)
        for direc in DIRS:
            try_point = point + direc
            if try_point in visited_points:
                continue
            if not (
                min_x <= try_point.x <= max_x
                and min_y <= try_point.y <= max_y
                and min_z <= try_point.z <= max_z
            ):
                continue
            if try_point in points:
                real_surface_count += 1
                continue
            to_check.add(try_point)
    return real_surface_count


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    SENSORS = {Pos(*map(int, line.split(","))) for line in DATA.split("\n")}

    print(part_1(SENSORS))
    print(part_2(SENSORS))
