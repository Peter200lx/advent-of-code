from pathlib import Path
from typing import List, Dict, Tuple, NamedTuple


class Point(NamedTuple):
    y: int
    x: int


DIRECTIONS = {"U": Point(1, 0), "D": Point(-1, 0), "R": Point(0, 1), "L": Point(0, -1)}


def build_wire_points(wire_list: List[str]) -> Dict[Point, int]:
    current_point = Point(0, 0)
    distance_so_far = 0
    loc_dict = {current_point: distance_so_far}
    for direction in wire_list:
        arrow = direction[0]
        distance = int(direction[1:])
        for i in range(1, distance + 1):
            current_point = Point(
                current_point.y + DIRECTIONS[arrow].y,
                current_point.x + DIRECTIONS[arrow].x,
            )

            if current_point not in loc_dict:
                loc_dict[current_point] = distance_so_far + i
        distance_so_far += distance
    return loc_dict


def find_cross(two_wires: List[List[str]]) -> Tuple[int, int]:
    wire1_dict = build_wire_points(two_wires[0])
    wire2_dict = build_wire_points(two_wires[1])
    crossing_points = set(wire1_dict) & set(wire2_dict)
    crossing_points.remove(Point(0, 0))
    min_man = 9e999
    min_steps = 9e999
    for point in crossing_points:
        man = abs(point.x) + abs(point.y)
        min_man = min(man, min_man)
        steps = wire1_dict[point] + wire2_dict[point]
        min_steps = min(steps, min_steps)
    return min_man, min_steps


if __name__ == "__main__":
    DATA = Path("day03.input").read_text().strip()
    str_list = [line.split(",") for line in DATA.split("\n")]

    print(find_cross(str_list))
