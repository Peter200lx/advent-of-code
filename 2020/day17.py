from dataclasses import dataclass
from typing import Set, Type

DATA = """##......
.##...#.
.#######
..###.##
.#.###..
..#.####
##.####.
##..#.##"""


@dataclass(frozen=True)
class Coord:
    x: int
    y: int
    z: int

    @staticmethod
    def create_2d(x, y) -> "Coord":
        return Coord(x, y, 0)

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y, self.z + other.z)


@dataclass(frozen=True)
class Coord4D(Coord):
    x: int
    y: int
    z: int
    t: int

    @staticmethod
    def create_2d(x, y) -> "Coord4D":
        return Coord4D(x, y, 0, 0)

    def __add__(self, other: "Coord4D") -> "Coord4D":
        return Coord4D(self.x + other.x, self.y + other.y, self.z + other.z, self.t + other.t)


COORD_NEIGHBORS = [
    Coord(x, y, z) for x in range(-1, 2) for y in range(-1, 2) for z in range(-1, 2) if (x, y, z) != (0, 0, 0)
]
COORD4D_NEIGHBORS = [
    Coord4D(x, y, z, t)
    for x in range(-1, 2)
    for y in range(-1, 2)
    for z in range(-1, 2)
    for t in range(-1, 2)
    if (x, y, z, t) != (0, 0, 0, 0)
]


class Map:
    def __init__(self, space: Set[Coord]):
        self.space = space
        assert self.space, "Next step is bad if no items in set"
        if isinstance(next(iter(self.space)), Coord4D):
            self.neighbor_dirs = COORD4D_NEIGHBORS
        else:
            self.neighbor_dirs = COORD_NEIGHBORS
        self.checked_locs = set()

    @staticmethod
    def load(lines: str, point_class: Type[Coord]):
        space = set()
        for y, line in enumerate(lines.split("\n")):
            for x, c in enumerate(line):
                if c == "#":
                    space.add(point_class.create_2d(x, y))
        return Map(space)

    def next_state(self, loc: Coord, new_set: Set[Coord]):
        self.checked_locs.add(loc)
        active_n = 0
        for direction in self.neighbor_dirs:
            neighbor = loc + direction
            if neighbor in self.space:
                active_n += 1

            if loc in self.space and neighbor not in self.checked_locs:
                self.next_state(neighbor, new_set)

        if loc in self.space:
            if active_n in (2, 3):
                new_set.add(loc)
        else:
            if active_n == 3:
                new_set.add(loc)

    def run_cycle(self):
        new_set = set()
        for loc in self.space:
            if loc not in self.checked_locs:
                self.next_state(loc, new_set)
        return Map(new_set)

    def count(self):
        return len(self.space)

    def print_z_n(self, z: int = 0):
        minx = min(l.x for l in self.space)
        maxx = max(l.x for l in self.space)
        miny = min(l.y for l in self.space)
        maxy = max(l.y for l in self.space)
        for y in range(miny, maxy + 1):
            print("".join("#" if Coord(x, y, z) in self.space else "." for x in range(minx, maxx + 1)))


if __name__ == "__main__":
    cubes_3d = Map.load(DATA, Coord)
    for _ in range(6):
        cubes_3d = cubes_3d.run_cycle()
    print(cubes_3d.count())

    cubes_4d = Map.load(DATA, Coord4D)
    for _ in range(6):
        cubes_4d = cubes_4d.run_cycle()
    print(cubes_4d.count())
