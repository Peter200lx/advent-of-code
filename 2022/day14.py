from enum import Enum
from pathlib import Path
from typing import NamedTuple, Union, Dict, List, Optional

INPUT_FILE = Path(__file__).with_suffix(".input")


class Slice(NamedTuple):
    y: Union[range, int]
    x: Union[range, int]

    def gen(self):
        if isinstance(self.y, int) and isinstance(self.x, range):
            yield from (Coord(self.y, x) for x in self.x)
        elif isinstance(self.y, range) and isinstance(self.x, int):
            yield from (Coord(y, self.x) for y in self.y)


class Coord(NamedTuple):
    y: int
    x: int


class Range(NamedTuple):
    y_min: int
    y_max: int
    x_min: int
    x_max: int


SOURCE = Coord(y=0, x=500)


class FieldTypes(Enum):
    ROCK = -1
    EMPTY = 0
    SAND_FALLING = 1
    SAND_STATIONARY = 2
    SOURCE = 8


FIELD_PRINT = {
    FieldTypes.ROCK: "#",
    FieldTypes.EMPTY: ".",
    FieldTypes.SAND_STATIONARY: "o",
    FieldTypes.SAND_FALLING: "~",
    FieldTypes.SOURCE: "+",
}


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
                            y=range(min(start_y, end_y), max(start_y, end_y) + 1),
                            x=end_x,
                        )
                    )
                )
            elif start_y == end_y:
                data_list.append(
                    Slice(
                        y=end_y, x=range(min(start_x, end_x), max(start_x, end_x) + 1)
                    )
                )
    return data_list, Range(min_y - 1, max_y + 1 + 2, min_x - 1, max_x + 1)


class Field:
    def __init__(self, scan_list: List[Slice], frange: Range, source: Coord):
        self.range = frange
        self.point_cloud: Dict[Coord, FieldTypes] = {}
        for scan in scan_list:
            for point in scan.gen():
                self.point_cloud[point] = FieldTypes.ROCK
        self.falling_sand = set()
        self.point_cloud[source] = FieldTypes.SOURCE
        sand_loc = Coord(source.y + 1, source.x)
        self.falling_sand.add(source)
        self.falling_sand.add(sand_loc)
        self.point_cloud[sand_loc] = FieldTypes.SAND_FALLING

    def print(self):
        for y in range(0, self.range.y_max):
            print(
                "".join(
                    FIELD_PRINT[self.point_cloud[Coord(y, x)]]
                    if Coord(y, x) in self.point_cloud
                    else "."
                    for x in range(self.range.x_min - 1, self.range.x_max + 1)
                )
            )

    def loc_type(self, loc: Coord) -> FieldTypes:
        return self.point_cloud.get(loc, FieldTypes.EMPTY)

    def drop_sand(self, loc: Coord) -> Optional[Coord]:
        if loc not in self.falling_sand:
            self.falling_sand.add(loc)
        below_loc = Coord(loc.y + 1, loc.x)
        if below_loc.y == self.range.y_max:
            return
        while self.loc_type(below_loc) == FieldTypes.EMPTY:
            self.point_cloud[below_loc] = FieldTypes.SAND_FALLING
            self.falling_sand.add(below_loc)
            below_loc = Coord(below_loc.y + 1, below_loc.x)
            if below_loc.y == self.range.y_max:
                return
        return below_loc

    def fill_angle(self, orig_loc: Coord, direc: int):
        point_array = []
        new_point = Coord(y=orig_loc.y + 1, x=orig_loc.x + direc)
        while self.loc_type(new_point) is FieldTypes.EMPTY:
            self.point_cloud[new_point] = FieldTypes.SAND_FALLING
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
                self.point_cloud[p] = FieldTypes.SAND_STATIONARY
            return True

    def pile(self, loc: Coord):
        left_stationary = self.fill_angle(loc, direc=-1)
        if left_stationary:
            right_stationary = self.fill_angle(loc, direc=+1)
            if right_stationary:
                self.point_cloud[loc] = FieldTypes.SAND_STATIONARY

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


def run_simulation(field: Field) -> int:
    while field.step_sand():
        pass
    # field.print()
    return sum(v == FieldTypes.SAND_STATIONARY for v in field.point_cloud.values())


def run_floor_simulation(field: Field) -> int:
    for x in range(field.range.x_min - 2000, field.range.x_max + 2000):
        field.point_cloud[Coord(y=field.range.y_max - 1, x=x)] = FieldTypes.ROCK

    while field.step_sand():
        pass
    # field.print()
    return sum(v == FieldTypes.SAND_STATIONARY for v in field.point_cloud.values())


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    SCAN_OUTPUT, RANGE = parse_input(DATA)
    GROUND = Field(SCAN_OUTPUT, RANGE, SOURCE)
    print(run_simulation(GROUND))
    print(run_floor_simulation(GROUND))
