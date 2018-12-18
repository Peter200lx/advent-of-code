import re
from collections import namedtuple
from enum import Enum

import numpy as np

with open("day17.input", "r") as in_file:
    DATA = in_file.read()


EXAMPLE_DATA = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""


Slice = namedtuple("Slice", ["y", "x"])
Coord = namedtuple("Coord", ["y", "x"])
Range = namedtuple("Range", ["y_min", "y_max", "x_min", "x_max"])
RE_NUMS = re.compile(r"-?\d+")
SOURCES = [Coord(0, 500)]


class FieldTypes(Enum):
    CLAY = -1
    EMPTY = 0
    WATER_FALLING = 1
    WATER_STANDING = 2
    SOURCE = 8


FIELD_PRINT = {
    FieldTypes.CLAY.value: "#",
    FieldTypes.EMPTY.value: ".",
    FieldTypes.WATER_STANDING.value: "~",
    FieldTypes.WATER_FALLING.value: "|",
    FieldTypes.SOURCE.value: "+",
}


np.set_printoptions(
    linewidth=500, threshold=np.nan, formatter={"int": lambda x: FIELD_PRINT[x]}
)


def parse_input(data_blob):
    data_list = []
    min_x = 500
    max_x = 500
    min_y = 500
    max_y = 1
    for line in data_blob.strip().split("\n"):
        first, second_start, second_end = list(map(int, RE_NUMS.findall(line)))
        if line[0] == "x":
            min_x = min(min_x, first)
            max_x = max(max_x, first)
            min_y = min(min_y, second_start)
            max_y = max(max_y, second_end)
            data_list.append(Slice(slice(second_start, second_end + 1), first))
        else:
            min_x = min(min_x, second_start)
            max_x = max(max_x, second_end)
            max_y = max(max_y, first)
            min_y = min(min_y, first)
            data_list.append(Slice(first, slice(second_start, second_end + 1)))
    return data_list, Range(min_y - 1, max_y + 1, min_x - 1, max_x + 1)


class Field:
    def __init__(self, scan_list, frange, source_locs):
        self.range = frange
        self.array = np.zeros(
            (self.range.y_max + 1, self.range.x_max + 1), dtype=np.int32
        )
        for scan in scan_list:
            self.array[scan] = FieldTypes.CLAY.value
        self.falling_water = set()
        for loc in source_locs:
            self.array[loc] = FieldTypes.SOURCE.value
            water_loc = Coord(loc.y + 1, loc.x)
            self.falling_water.add(water_loc)
            self.array[water_loc] = FieldTypes.WATER_FALLING.value

    def print(self):
        print(self.array[:, soil_range.x_min - 1 :])

    def loc_type(self, loc):
        return FieldTypes(self.array[loc])

    def drop_water(self, loc):
        if loc not in self.falling_water:
            self.falling_water.add(loc)
        below_loc = Coord(loc.y + 1, loc.x)
        if below_loc.y == self.range.y_max:
            return False
        while self.loc_type(below_loc) == FieldTypes.EMPTY:
            self.array[below_loc] = FieldTypes.WATER_FALLING.value
            self.falling_water.add(below_loc)
            below_loc = Coord(below_loc.y + 1, below_loc.x)
            if below_loc.y == self.range.y_max:
                return False
        return below_loc

    def fill_dir(self, orig_loc, x_val_iter):
        for x in x_val_iter:
            my_loc = Coord(orig_loc.y, x)
            if self.loc_type(my_loc) is FieldTypes.CLAY:
                return x
            self.array[my_loc] = FieldTypes.WATER_FALLING.value
            self.falling_water.discard(my_loc)
            below_type = self.loc_type(Coord(orig_loc.y + 1, x))
            if below_type is FieldTypes.WATER_FALLING:
                return
            elif below_type is FieldTypes.EMPTY:
                self.drop_water(Coord(orig_loc.y, x))
                return

    def fill(self, loc):
        right_clay = self.fill_dir(loc, range(loc.x + 1, self.range.x_max + 1))
        left_clay = self.fill_dir(loc, range(loc.x - 1, self.range.x_min - 1, -1))
        if left_clay and right_clay:
            self.array[loc.y, left_clay + 1: right_clay] = FieldTypes.WATER_STANDING.value
            self.falling_water.remove(loc)
        return False

    def step_water(self):
        old_set = self.falling_water.copy()
        for loc in sorted(self.falling_water, reverse=True):
            if loc not in self.falling_water:
                continue
            if loc.y + 1 == self.range.y_max:
                self.falling_water.remove(loc)
                continue
            below_type = self.loc_type(Coord(loc.y + 1, loc.x))
            if below_type in (FieldTypes.CLAY, FieldTypes.WATER_STANDING):
                self.fill(loc)
            elif below_type is FieldTypes.EMPTY:
                self.drop_water(loc)
        return old_set != self.falling_water


def run_simulation(field):
    while field.step_water():
        # print(sorted(field.falling_water, reverse=True))
        # input("{ENTER} to continue")
        pass
    # field.print()
    print(
        (field.array == FieldTypes.WATER_STANDING.value).sum()
        + (field.array == FieldTypes.WATER_FALLING.value).sum()
        - field.range.y_min
    )
    print((field.array == FieldTypes.WATER_STANDING.value).sum())


if __name__ == '__main__':
    scan_output, soil_range = parse_input(DATA)
    soil = Field(scan_output, soil_range, SOURCES)
    run_simulation(soil)
