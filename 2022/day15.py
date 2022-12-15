import re
from pathlib import Path
from typing import List, NamedTuple, Set

INPUT_FILE = Path(__file__).with_suffix(".input")

RE_NUMS = re.compile(r"-?\d+")

P1_Y = 2000000


class Pos(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Pos") -> "Pos":
        return Pos(self.x + other.x, self.y + other.y)

    def mann(self, other: "Pos") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


P2_MIN = Pos(0, 0)
P2_MAX = Pos(4000000, 4000000)


class Sensor:
    def __init__(self, line: str):
        s_x, s_y, b_x, b_y = tuple(map(int, RE_NUMS.findall(line)))
        self.loc = Pos(s_x, s_y)
        self.b_loc = Pos(b_x, b_y)
        self.dist = self.loc.mann(self.b_loc)

    def __repr__(self):
        return f"Sensor(loc={self.loc}, dist={self.dist})"

    def filled_space(self, y_line: int) -> Set[Pos]:
        cross_point = Pos(self.loc.x, y_line)
        invalid_points = set()
        if self.loc.mann(cross_point) <= self.dist:
            invalid_points.add(cross_point)
            for i in range(9999999):
                l_point = Pos(cross_point.x - i, y_line)
                r_point = Pos(cross_point.x + i, y_line)
                if self.loc.mann(l_point) <= self.dist:
                    invalid_points.add(l_point)
                if self.loc.mann(r_point) <= self.dist:
                    invalid_points.add(r_point)
                else:
                    break
        invalid_points.discard(self.b_loc)
        return invalid_points

    def just_outside_points(self, min_loc: Pos, max_loc: Pos) -> Set[Pos]:
        just_outside: Set[Pos] = set()
        cur_loc = Pos(self.loc.x, self.loc.y - self.dist - 1)
        for direc in (Pos(1, 1), Pos(-1, 1), Pos(-1, -1), Pos(1, -1)):
            if (
                min_loc.x <= cur_loc.x <= max_loc.x
                and min_loc.y <= cur_loc.y <= max_loc.y
            ):
                just_outside.add(cur_loc)
            cur_loc += direc
            while not (cur_loc.x == self.loc.x or cur_loc.y == self.loc.y):
                if (
                    min_loc.x <= cur_loc.x <= max_loc.x
                    and min_loc.y <= cur_loc.y <= max_loc.y
                ):
                    just_outside.add(cur_loc)
                cur_loc += direc
        return just_outside


def part_2(sensors: List[Sensor]) -> int:
    for sensor in sensors:
        to_try = sensor.just_outside_points(P2_MIN, P2_MAX)
        print(f"On Sensor {sensor.loc} trying {len(to_try)} points")
        for point in to_try:
            bad_point = False
            for other_s in sensors:
                if other_s == sensor:
                    continue
                if other_s.loc.mann(point) <= other_s.dist:
                    bad_point = True
                    break
            if not bad_point:
                print(f"Found good point {point}")
                return point.x * 4000000 + point.y


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    SENSORS = [Sensor(line) for line in DATA.split("\n")]

    print(len(set.union(*(s.filled_space(P1_Y) for s in SENSORS))))
    print(part_2(SENSORS))
