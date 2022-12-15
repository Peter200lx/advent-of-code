import re
from pathlib import Path
from typing import List, NamedTuple, Set, Optional

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

    def in_range(self, other: "Sensor") -> bool:
        if other == self:
            return False
        return self.loc.mann(other.loc) <= self.dist + other.dist + 1

    def __repr__(self):
        return f"Sensor(loc={self.loc}, dist={self.dist})"

    def filled_space(self, y_line: int) -> Optional[range]:
        cross_point = Pos(self.loc.x, y_line)
        cpoint_mann = self.loc.mann(cross_point)
        if cpoint_mann <= self.dist:
            x_dist = self.dist - abs(y_line - self.loc.y)
            return range(self.loc.x - x_dist, self.loc.x + x_dist + 1)
        return

    def just_outside_points(self, min_loc: Pos, max_loc: Pos) -> Set[Pos]:
        just_outside: Set[Pos] = set()
        cur_x, cur_y = self.loc.x, self.loc.y - self.dist - 1
        for direc in (Pos(1, 1), Pos(-1, 1), Pos(-1, -1), Pos(1, -1)):
            if min_loc.x <= cur_x <= max_loc.x and min_loc.y <= cur_y <= max_loc.y:
                just_outside.add(Pos(cur_x, cur_y))
            cur_x, cur_y = cur_x + direc.x, cur_y + direc.y
            while not (cur_x == self.loc.x or cur_y == self.loc.y):
                if min_loc.x <= cur_x <= max_loc.x and min_loc.y <= cur_y <= max_loc.y:
                    just_outside.add(Pos(cur_x, cur_y))
                cur_x, cur_y = cur_x + direc.x, cur_y + direc.y
        return just_outside


def collapse_ranges(all_ranges: List[range]) -> List[range]:
    all_ranges.sort(key=lambda x: x.start)
    final_ranges = []
    cur_range: range = all_ranges[0]
    for i in range(len(all_ranges) - 1):
        next_range = all_ranges[i + 1]
        if cur_range.start in next_range or next_range.start in cur_range:
            cur_range = range(cur_range.start, max(cur_range.stop, next_range.stop))
        else:
            final_ranges.append(cur_range)
            cur_range = next_range
    final_ranges.append(cur_range)
    return final_ranges


def part_1(sensors: List[Sensor], target_y: int) -> int:
    all_ranges = [
        r for r in (s.filled_space(target_y) for s in sensors) if r is not None
    ]
    ranges = collapse_ranges(all_ranges)
    beacons_in_range = {
        s.b_loc.x
        for s in sensors
        for r in ranges
        if s.b_loc.y == target_y and s.b_loc.x in r
    }
    return sum(len(r) for r in ranges) - len(beacons_in_range)


def part_2(sensors: List[Sensor]) -> int:
    for sensor in sensors:
        to_try = sensor.just_outside_points(P2_MIN, P2_MAX)
        print(f"On Sensor {sensor.loc} trying {len(to_try)} points")
        close_sensors = [s for s in sensors if sensor.in_range(s)]
        for point in to_try:
            bad_point = False
            for other_s in close_sensors:
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

    print(part_1(SENSORS, P1_Y))
    print(part_2(SENSORS))
