from math import gcd
import re
from functools import reduce
from typing import List, Tuple, Union, Optional

DATA = """
<x=13, y=-13, z=-2>
<x=16, y=2, z=-15>
<x=7, y=-18, z=-12>
<x=-3, y=-8, z=-8>""".strip()

RE_NUMS = re.compile(r"-?\d+")


def new_velocity(locations, velocities):
    for i, first in enumerate(locations):
        for j, second in enumerate(locations):
            if i == j:
                continue
            if first > second:
                velocities[i] += -1
            elif first < second:
                velocities[i] += 1
    return velocities


def new_locations(locations, velocities):
    for i, v in enumerate(velocities):
        locations[i] += v


def axis_period(
    starting_locations: List[int], stop_count: Optional[int] = None
) -> Union[int, Tuple[List[int], List[int]]]:
    locations = starting_locations[:]
    starting_velocities = [0] * len(locations)
    velocities = starting_velocities[:]
    count = 0
    while True:
        new_velocity(locations, velocities)
        new_locations(locations, velocities)
        count += 1
        if count == stop_count:
            return locations, velocities
        if locations == starting_locations and velocities == starting_velocities:
            return count


def part1(moons: List[Tuple[int, ...]], cycles: int = 1000) -> int:
    xl, xv = axis_period([m[0] for m in moons], cycles)
    yl, yv = axis_period([m[1] for m in moons], cycles)
    zl, zv = axis_period([m[2] for m in moons], cycles)
    lsum = [sum(abs(n) for n in c) for c in zip(xl, yl, zl)]
    vsum = [sum(abs(n) for n in c) for c in zip(xv, yv, zv)]
    moon_energy = [cl * cv for cl, cv in zip(lsum, vsum)]
    return sum(moon_energy)


def part2(moons: List[Tuple[int, ...]]):
    x_period = axis_period([m[0] for m in moons])
    y_period = axis_period([m[1] for m in moons])
    z_period = axis_period([m[2] for m in moons])
    # Calculate the LCM as suggested by https://stackoverflow.com/a/55773512/1038644
    return reduce(lambda a, b: a * b // gcd(a, b), (x_period, y_period, z_period))


if __name__ == "__main__":
    starting_moons = [
        tuple(map(int, RE_NUMS.findall(line))) for line in DATA.split("\n")
    ]
    print(part1(starting_moons))
    print(part2(starting_moons))
