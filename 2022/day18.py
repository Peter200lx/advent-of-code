import re
from pathlib import Path
from typing import List, NamedTuple, Set, Optional

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


def fill_sealed(group: Set[Pos]):
    print(f"{group=}")
    min_x, max_x = min(p.x for p in group), max(p.x for p in group)
    min_y, max_y = min(p.y for p in group), max(p.y for p in group)
    min_z, max_z = min(p.z for p in group), max(p.z for p in group)
    tested_points: Set[Pos] = set()
    while True:
        tri_point = None
        for point in group:
            for direc in DIRS:
                try_point = point + direc
                if try_point in group or try_point in tested_points:
                    continue
                if not (
                    min_x <= try_point.x <= max_x
                    and min_y <= try_point.y <= max_y
                    and min_z <= try_point.z <= max_z
                ):
                    continue
                print(f"{try_point=} {sum((try_point+d) in group for d in DIRS)}")
                if sum((try_point + d) in group for d in DIRS) >= 3:
                    tri_point = try_point
                    break
            if tri_point:
                break
        if tri_point is None:
            print(f"Failed to find tri-point")
            break
        print(tri_point)
        to_check = {tri_point}
        my_group: Set[Pos] = set()
        good_path = True
        while to_check:
            cur_point = to_check.pop()
            tested_points.add(cur_point)
            my_group.add(cur_point)
            for direc in DIRS:
                try_point = cur_point + direc
                if not (
                    min_x <= try_point.x <= max_x
                    and min_y <= try_point.y <= max_y
                    and min_z <= try_point.z <= max_z
                ):
                    good_path = False
                    continue
                if try_point in group or try_point in tested_points:
                    continue
                print(f"Group added {try_point}")
                to_check.add(try_point)
            to_check.discard(cur_point)
        if good_path:
            group.update(my_group)
        print(f"Next Group")


def part_2_bad_grouping(points: Set[Pos]):
    point_cloud = set(points)
    connected_groups: List[Set[Pos]] = []
    while point_cloud:
        next_point = point_cloud.pop()
        to_scan = {next_point}
        scanned: Set[Pos] = set()
        while to_scan:
            cur_point = to_scan.pop()
            for direc in DIRS:
                adj_point = cur_point + direc
                if adj_point in scanned:
                    continue
                if adj_point in point_cloud:
                    point_cloud.discard(adj_point)
                    to_scan.add(adj_point)
            scanned.add(cur_point)
        connected_groups.append(scanned)
    for group in connected_groups:
        if len(group) >= 6:  # len(DIRS) to enclose
            fill_sealed(group)
    return sum(part_1(g) for g in connected_groups)


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
