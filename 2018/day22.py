from collections import namedtuple
from heapq import heappop, heappush
from typing import Dict, List, Set

import numpy as np

DATA = """depth: 11739
target: 11,718"""
DATA_DEPTH = 11739
Coord = namedtuple("Coord", ["y", "x"])
DATA_TARGET = Coord(x=11, y=718)

# Region
ROCKY = 0
WET = 1
NARROW = 2

# Tools
TORCH = 3
GEAR = 4
NEITHER = 5

TOOL_TYPE = {
    TORCH: "Torch",
    GEAR: "Climbing Gear",
    NEITHER: "Neither Tool",
}

MAP_TYPE = {
    ROCKY: ".",
    WET: "=",
    NARROW: "|",
}

np.set_printoptions(linewidth=300, threshold=np.nan)

REGION_TO_TOOL = {
    ROCKY: {GEAR, TORCH},
    WET: {GEAR, NEITHER},
    NARROW: {TORCH, NEITHER},
}


TOOL_TO_REGION = {
    TORCH: {ROCKY, NARROW},
    GEAR: {ROCKY, WET},
    NEITHER: {WET, NARROW},
}


def build_soil(depth: int, target: Coord, bonus_size: int = 10) -> np.ndarray:
    field_size = Coord(target.y + bonus_size, target.x + bonus_size)
    erosion = {}
    for iy, ix in np.ndindex(field_size):
        if ix == 0 and iy == 0:
            geo_index = 0
        elif iy == target.y and ix == target.x:
            geo_index = 0
        elif iy == 0:
            geo_index = ix * 16807
        elif ix == 0:
            geo_index = iy * 48271
        else:
            geo_index = erosion[iy, ix - 1] * erosion[iy - 1, ix]
        erosion[Coord(iy, ix)] = (geo_index + depth) % 20183

    def field_type(y, x):
        return erosion[y, x] % 3

    field_type_vector = np.vectorize(field_type)
    return np.fromfunction(field_type_vector, field_size, dtype=np.int32)


def init_tool_heatmaps(field: np.ndarray) -> Dict[int, np.ndarray]:
    tool_heatmap = {}

    def tool_type_wrapper(base_field, tool):
        def tool_type(y, x):
            return 1e9 if base_field[y, x] in TOOL_TO_REGION[tool] else -1
        return tool_type

    for t in (TORCH, GEAR, NEITHER):
        tool_type_vector = np.vectorize(tool_type_wrapper(field, t))
        tool_heatmap[t] = np.fromfunction(tool_type_vector, field.shape, dtype=np.int32)

    return tool_heatmap


def adjacent_locs(field: np.ndarray, loc: Coord) -> Set[Coord]:
    possible_locs = set()
    if loc.y > 0:
        possible_locs.add(Coord(loc.y - 1, loc.x))
    if loc.x > 0:
        possible_locs.add(Coord(loc.y, loc.x - 1))
    if loc.x < field.shape[1] - 1:
        possible_locs.add(Coord(loc.y, loc.x + 1))
    if loc.y < field.shape[0] - 1:
        possible_locs.add(Coord(loc.y + 1, loc.x))
    return {l for l in possible_locs if field[l] > -1}


def simulate_water(t_field: np.ndarray, check_locs: Set[Coord], cost: int) -> Set[Coord]:
    updated_locs = set()
    next_locs = set()
    for loc in check_locs:
        if t_field[loc] == -1 or t_field[loc] <= cost:
            continue
        t_field[loc] = cost
        updated_locs.add(loc)
        next_locs |= adjacent_locs(t_field, loc)
    next_locs -= check_locs
    if next_locs:
        updated_locs |= simulate_water(t_field, next_locs, cost + 1)
    return updated_locs


ToCheck = namedtuple("ToCheck", ["start_cost", "loc", "tool"])


def step_tool(base_field: np.ndarray, tool_fields: Dict[int, np.ndarray], this_check: ToCheck) -> List[ToCheck]:
    t_field = tool_fields[this_check.tool]
    assert t_field[this_check.loc] >= 0
    active_locations = simulate_water(t_field, {this_check.loc}, this_check.start_cost)
    ret_checks = []
    for loc in active_locations:
        new_tool = [t for t in REGION_TO_TOOL[base_field[loc]] if t != this_check.tool][0]
        new_cost = t_field[loc] + 7
        if tool_fields[new_tool][loc] > new_cost:
            ret_checks.append(ToCheck(new_cost, loc, new_tool))
    return ret_checks


def part_2(field: np.ndarray, target: Coord) -> int:
    tool_heatmaps = init_tool_heatmaps(field)
    # for tool in tool_heatmaps:
    #     print(TOOL_TYPE[tool])
    #     print(tool_heatmaps[tool])
    first_check = ToCheck(0, Coord(0, 0), TORCH)
    heap = []
    for check in step_tool(field, tool_heatmaps, first_check):
        heappush(heap, check)
    # count = 0
    while heap:
        to_check = heappop(heap)
        if tool_heatmaps[to_check.tool][to_check.loc] < to_check.start_cost:
            continue
        # count += 1
        # if count % 1000 == 0:
        #     print(count, to_check)
        for check in step_tool(field, tool_heatmaps, to_check):
            heappush(heap, check)
    # for tool in tool_heatmaps:
    #     print(TOOL_TYPE[tool])
    #     print(tool_heatmaps[tool][target])
    #     print(tool_heatmaps[tool])
    return int(tool_heatmaps[TORCH][target])


if __name__ == '__main__':
    # DATA_DEPTH = 510
    # DATA_TARGET = Coord(10, 10)

    grounds = build_soil(DATA_DEPTH, DATA_TARGET, 21)
    if tuple(int(i) for i in np.__version__.split(".") if i.isdigit()) >= (1, 15):
        with np.printoptions(formatter={"int": lambda x: MAP_TYPE[x]}):
            print(grounds)
    else:
        print(grounds)
    print(grounds[:DATA_TARGET.y + 1, :DATA_TARGET.x + 1].sum())
    print(part_2(grounds, DATA_TARGET))
