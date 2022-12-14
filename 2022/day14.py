import re
import sys
from enum import Enum
from pathlib import Path
from typing import NamedTuple, Union

import numpy as np

INPUT_FILE = Path(__file__).with_suffix(".input")


class Slice(NamedTuple):
    y: Union[slice, int]
    x: Union[slice, int]


class Coord(NamedTuple):
    y: int
    x: int


class Range(NamedTuple):
    y_min: int
    y_max: int
    x_min: int
    x_max: int


RE_NUMS = re.compile(r"-?\d+")
SOURCES = [Coord(y=0, x=500)]


class FieldTypes(Enum):
    ROCK = -1
    EMPTY = 0
    SAND_FALLING = 1
    SAND_STATIONARY = 2
    SOURCE = 8


FIELD_PRINT = {
    FieldTypes.ROCK.value: "#",
    FieldTypes.EMPTY.value: ".",
    FieldTypes.SAND_STATIONARY.value: "o",
    FieldTypes.SAND_FALLING.value: "~",
    FieldTypes.SOURCE.value: "+",
}


np.set_printoptions(
    linewidth=500, threshold=sys.maxsize, formatter={"int": lambda x: FIELD_PRINT[x]}
)


def parse_input(data_blob):
    data_list = []
    min_x = 500
    max_x = 500
    min_y = 500
    max_y = 1
    for line in data_blob.strip().split("\n"):
        point_strs = line.split(" -> ")
        for i in range(len(point_strs) - 1):
            start_x, start_y = list(map(int, point_strs[i].split(",")))
            end_x, end_y = list(map(int, point_strs[i + 1].split(",")))
            min_x = min(min_x, start_x, end_x)
            min_y = min(min_y, start_y, end_y)
            max_x = max(max_x, start_x, end_x)
            max_y = max(max_y, start_y, end_y)
            if start_x == end_x:
                data_list.append(
                    (
                        Slice(
                            y=slice(min(start_y, end_y), max(start_y, end_y) + 1),
                            x=end_x,
                        )
                    )
                )
            elif start_y == end_y:
                data_list.append(
                    Slice(
                        y=end_y, x=slice(min(start_x, end_x), max(start_x, end_x) + 1)
                    )
                )
    return data_list, Range(min_y - 1, max_y + 1 + 2, min_x - 1, max_x + 1)


class Field:
    def __init__(self, scan_list, frange, source_locs):
        self.range = frange
        self.array = np.zeros((frange.y_max, frange.x_max), dtype=np.int8)
        for scan in scan_list:
            self.array[scan] = FieldTypes.ROCK.value
        self.falling_sand = set()
        for loc in source_locs:
            self.array[loc] = FieldTypes.SOURCE.value
            sand_loc = Coord(loc.y + 1, loc.x)
            self.falling_sand.add(sand_loc)
            self.array[sand_loc] = FieldTypes.SAND_FALLING.value

    def print(self):
        print(self.array[:, self.range.x_min - 1 :])

    def loc_type(self, loc):
        return FieldTypes(self.array[loc])

    def drop_sand(self, loc):
        if loc not in self.falling_sand:
            self.falling_sand.add(loc)
        below_loc = Coord(loc.y + 1, loc.x)
        if below_loc.y == self.range.y_max:
            return False
        while self.loc_type(below_loc) == FieldTypes.EMPTY:
            self.array[below_loc] = FieldTypes.SAND_FALLING.value
            self.falling_sand.add(below_loc)
            below_loc = Coord(below_loc.y + 1, below_loc.x)
            if below_loc.y == self.range.y_max:
                return False
        return below_loc

    def fill_angle(self, orig_loc: Coord, direc: int):
        point_array = []
        new_point = Coord(y=orig_loc.y + 1, x=orig_loc.x + direc)
        while self.loc_type(new_point) is FieldTypes.EMPTY:
            self.array[new_point] = FieldTypes.SAND_FALLING.value
            self.falling_sand.add(new_point)
            below_loc = Coord(new_point.y + 1, new_point.x)
            if below_loc.y == self.range.y_max:
                return False
            below_type = self.loc_type(below_loc)
            if below_type is FieldTypes.SAND_FALLING:
                return False
            elif below_type is FieldTypes.EMPTY:
                self.drop_sand(new_point)
                return False
            point_array.append(new_point)
            new_point = Coord(y=new_point.y + 1, x=new_point.x + direc)
        if self.loc_type(new_point) in (FieldTypes.ROCK, FieldTypes.SAND_STATIONARY):
            for p in point_array:
                self.falling_sand.discard(p)
                self.array[p] = FieldTypes.SAND_STATIONARY.value
            return True

    def pile(self, loc: Coord):
        left_stationary = self.fill_angle(loc, direc=-1)
        if left_stationary:
            right_stationary = self.fill_angle(loc, direc=+1)
            if right_stationary:
                self.array[loc] = FieldTypes.SAND_STATIONARY.value

    def step_sand(self):
        old_set = self.falling_sand.copy()
        for loc in sorted(self.falling_sand, reverse=True):
            if loc not in self.falling_sand:
                continue
            if loc.y + 1 == self.range.y_max:
                self.falling_sand.remove(loc)
                continue
            below_type = self.loc_type(Coord(loc.y + 1, loc.x))
            if below_type in (FieldTypes.ROCK, FieldTypes.SAND_STATIONARY):
                self.pile(loc)
            elif below_type is FieldTypes.EMPTY:
                self.drop_sand(loc)
        return old_set != self.falling_sand


def run_simulation(field):
    while field.step_sand():
        pass
    field.print()
    return (field.array == FieldTypes.SAND_STATIONARY.value).sum()


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    DAdTA = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

    SCAN_OUTPUT, RANGE = parse_input(DATA)
    GROUND = Field(SCAN_OUTPUT, RANGE, SOURCES)
    print(run_simulation(GROUND))
