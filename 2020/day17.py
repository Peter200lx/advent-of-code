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

    @staticmethod
    def load(lines: str, point_class: Type[Coord]):
        space = set()
        for y, line in enumerate(lines.split("\n")):
            for x, c in enumerate(line):
                if c == "#":
                    space.add(point_class.create_2d(x, y))
        return Map(space)

    def next_state(self, loc: Coord) -> bool:
        neighbors = {loc + direction for direction in self.neighbor_dirs}
        active_n = len(neighbors & self.space)

        if loc in self.space:
            if active_n in (2, 3):
                return True
        else:
            if active_n == 3:
                return True
        return False

    def run_cycle(self):
        all_to_check = {loc + direction for loc in self.space for direction in self.neighbor_dirs}
        new_set = {loc for loc in all_to_check if self.next_state(loc)}
        return Map(new_set)

    def count(self):
        return len(self.space)

    def print_2d_layer(self, z: int = 0, t: int = 0):
        minx, maxx = min(loc.x for loc in self.space), max(loc.x for loc in self.space)
        miny, maxy = min(loc.y for loc in self.space), max(loc.y for loc in self.space)

        if isinstance(next(iter(self.space)), Coord4D):

            def new_c(nx, ny):
                return Coord4D(nx, ny, z, t)

        else:
            assert t == 0, "Can't manipulate time in 3D space"

            def new_c(nx, ny):
                return Coord(nx, ny, z)

        for y in range(miny, maxy + 1):
            print("".join("#" if new_c(x, y) in self.space else "." for x in range(minx, maxx + 1)))


if __name__ == "__main__":
    cubes_3d = Map.load(DATA, Coord)
    for _ in range(6):
        cubes_3d = cubes_3d.run_cycle()
    print(cubes_3d.count())

    cubes_4d = Map.load(DATA, Coord4D)
    for _ in range(6):
        cubes_4d = cubes_4d.run_cycle()
    print(cubes_4d.count())
