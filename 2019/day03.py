from collections import namedtuple
from pathlib import Path

Point = namedtuple("Point", ["y", "x"])


def build_wire_points(wire_list):
    current_point = Point(0, 0)
    distance_so_far = 0
    loc_dict = {current_point: distance_so_far}
    for direction in wire_list:
        arrow = direction[0]
        distance = int(direction[1:])
        if arrow == "U":
            line_dict = {
                Point(current_point.y + y, current_point.x): distance_so_far + y
                for y in range(distance)
            }
            current_point = Point(current_point.y + distance, current_point.x)
        elif arrow == "D":
            line_dict = {
                Point(current_point.y - y, current_point.x): distance_so_far + y
                for y in range(distance)
            }
            current_point = Point(current_point.y - distance, current_point.x)
        elif arrow == "R":
            line_dict = {
                Point(current_point.y, current_point.x + x): distance_so_far + x
                for x in range(distance)
            }
            current_point = Point(current_point.y, current_point.x + distance)
        elif arrow == "L":
            line_dict = {
                Point(current_point.y, current_point.x - x): distance_so_far + x
                for x in range(distance)
            }
            current_point = Point(current_point.y, current_point.x - distance)
        else:
            raise ValueError(f"Unknown direction {direction}")
        distance_so_far += distance
        loc_dict = {**line_dict, **loc_dict}
    return loc_dict


def find_cross(two_wires):
    wire1_dict = build_wire_points(two_wires[0])
    wire2_dict = build_wire_points(two_wires[1])
    crossing_points = set(wire1_dict) & set(wire2_dict)
    crossing_points.remove(Point(0, 0))
    min_man = 9e999
    min_steps = 9e999
    for point in crossing_points:
        man = abs(0 - point.x) + abs(0 - point.y)
        min_man = min(man, min_man)
        steps = wire1_dict[point] + wire2_dict[point]
        min_steps = min(steps, min_steps)
    return min_man, min_steps


if __name__ == "__main__":
    DATA = Path("day03.input").read_text().strip()
    str_list = [[i for i in line.split(",")] for line in DATA.split("\n")]

    print(find_cross(str_list))
