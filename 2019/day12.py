from math import gcd
import re
from functools import reduce
from typing import NamedTuple, List, Set

DATA = """
<x=13, y=-13, z=-2>
<x=16, y=2, z=-15>
<x=7, y=-18, z=-12>
<x=-3, y=-8, z=-8>""".strip()

RE_NUMS = re.compile(r"-?\d+")


def compare_axis(myaxis, other_axis):
    if myaxis > other_axis:
        return -1
    elif myaxis < other_axis:
        return 1
    else:
        return 0


class Vector(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other) -> "Vector":
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)


class Moon(NamedTuple):
    pos: Vector
    vel: Vector

    def new_velocity(self, all_moons):
        new_velocity = list(self.vel)
        for moon in all_moons - {self}:
            for axis in range(3):
                new_velocity[axis] += compare_axis(self.pos[axis], moon.pos[axis])
        return Moon(self.pos, Vector(*new_velocity))

    def new_position(self):
        return Moon(self.pos + self.vel, self.vel)

    def energy(self):
        return self.pos.energy() * self.vel.energy()


def create_moon(line: str):
    x, y, z = tuple(map(int, RE_NUMS.findall(line)))
    return Moon(Vector(x, y, z), Vector(0, 0, 0))


def simulate_gravity(moons: Set[Moon]):
    new_moon_velocities = set()
    for moon in moons:
        new_moon_velocities.add(moon.new_velocity(moons))
    new_moon_locations = set()
    for moon in new_moon_velocities:
        new_moon_locations.add(moon.new_position())
    return new_moon_locations


def part1(moons, cycles: int = 1000):
    for i in range(cycles):
        moons = simulate_gravity(moons)
    return sum(m.energy() for m in moons)


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


def axis_period(starting_locations: List[int]):
    locations = starting_locations[:]
    starting_velocities = [0] * len(locations)
    velocities = starting_velocities[:]
    count = 0
    while True:
        new_velocity(locations, velocities)
        new_locations(locations, velocities)
        count += 1
        if locations == starting_locations and velocities == starting_velocities:
            return count


def part2(moons: Set[Moon]):
    x_period = axis_period([m.pos.x for m in moons])
    y_period = axis_period([m.pos.y for m in moons])
    z_period = axis_period([m.pos.z for m in moons])
    # Calculate the LCM as suggested by https://stackoverflow.com/a/55773512/1038644
    return reduce(lambda a, b: a * b // gcd(a, b), (x_period, y_period, z_period))


if __name__ == "__main__":
    all_moons = {create_moon(line) for line in DATA.split("\n")}
    print(part1(all_moons))
    print(part2(all_moons))
