from pathlib import Path
from typing import List, Dict, Tuple, NamedTuple


class Point(NamedTuple):
    y: int
    x: int


DIRECTIONS = {"U": Point(1, 0), "D": Point(-1, 0), "R": Point(0, 1), "L": Point(0, -1)}


def build_wire_points(wire_list: List[str]) -> Dict[Point, int]:
    current_point = Point(0, 0)
    distance_so_far = 0
    loc_dict = {}
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
    min_man = min(abs(p.x) + abs(p.y) for p in crossing_points)
    min_steps = min(wire1_dict[p] + wire2_dict[p] for p in crossing_points)
    return min_man, min_steps


if __name__ == "__main__":
    DATA = Path("day03.input").read_text().strip()
    str_list = [line.split(",") for line in DATA.split("\n")]

    print(find_cross(str_list))
