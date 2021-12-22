import re
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple, Dict, Set, List, Optional, Tuple

INPUT_FILE = Path(__file__).with_suffix(".input")

RE_NUMS = re.compile(r"-?\d+")


class Coord(NamedTuple):
    x: int
    y: int
    z: int

    def iter_to(self, other: "Coord"):
        minx, maxx = max(min(self.x, other.x), -50), min(max(self.x, other.x), 50) + 1
        miny, maxy = max(min(self.y, other.y), -50), min(max(self.y, other.y), 50) + 1
        minz, maxz = max(min(self.z, other.z), -50), min(max(self.z, other.z), 50) + 1
        yield from (
            (x, y, z)
            for x in range(minx, maxx)
            for y in range(miny, maxy)
            for z in range(minz, maxz)
        )

    def volume(self, other: "Coord"):
        return (
            (abs(self.x - other.x) + 1)
            * (abs(self.y - other.y) + 1)
            * (abs(self.z - other.z) + 1)
        )


class Cube(NamedTuple):
    on: bool
    c1: Coord
    c2: Coord

    @staticmethod
    def from_str(line: str) -> "Cube":
        on = line.split()[0] == "on"
        x0, x1, y0, y1, z0, z1 = tuple(map(int, RE_NUMS.findall(line)))
        assert x0 < x1 and y0 < y1 and z0 < z1
        return Cube(on, Coord(x0, y0, z0), Coord(x1, y1, z1))

    def modify_grid(self, grid: Set[Coord]):
        for x, y, z in self.c1.iter_to(self.c2):
            if (x, y, z) in grid:
                if not self.on:
                    grid.discard((x, y, z))
            else:
                if self.on:
                    grid.add(Coord(x, y, z))

    def non_overlap_1d(
        self, other: "Cube", dimension: int
    ) -> List[Tuple[bool, int, int]]:
        my_min, my_max = self.c1[dimension], self.c2[dimension]  # represented by []
        o_min, o_max = other.c1[dimension], other.c2[dimension]  # represented by ()
        if o_min > my_max or my_min > o_max:  # [--] (--)  ||  (--) [--]
            return []  # no overlap
        elif o_min <= my_min:  # (--[-
            if my_max <= o_max:  # (--[--]--)  I am contained
                return [
                    (False, o_min, my_min - 1),
                    (False, my_min, my_max),
                    (False, my_max + 1, o_max),
                ]
            elif o_max < my_max:  # (--[--)--]  Partial left
                return [(True, my_min, o_min - 1), (False, o_min, my_max)]
        elif my_min <= o_min:  # [--(-
            if o_max <= my_max:  # [--(--)--]  I contain
                return [
                    (True, my_min, o_min - 1),
                    (False, o_min, o_max),
                    (True, o_max + 1, my_max),
                ]
            elif my_max < o_max:  # [--(--]--)  partial right
                return [(False, my_min, o_max), (True, o_max + 1, my_max)]

    def yield_non_overlap(self, other: "Cube"):
        ranges = [self.non_overlap_1d(other, i) for i in range(3)]
        if any(not r for r in ranges):  # If no overlap, return self
            yield self
            return
        for xrange in ranges[0]:
            for yrange in ranges[1]:
                for zrange in ranges[2]:
                    # Skip entirely contained sections
                    if any(outside for outside, _min, _max in (xrange, yrange, zrange)):
                        yield Cube(
                            True,
                            *(Coord(xrange[i], yrange[i], zrange[i]) for i in (1, 2)),
                        )

    def overlap_1d(
        self, other: Tuple[Coord, Coord], dimension: int
    ) -> Optional[Tuple[int, int]]:
        my_min, my_max = self.c1[dimension], self.c2[dimension]  # represented by []
        o_min, o_max = other[0][dimension], other[1][dimension]  # represented by ()
        if o_min > my_max or my_min > o_max:  # [--] (--)  ||  (--) [--]
            return None  # no overlap
        return max(o_min, my_min), min(o_max, my_max)

    def overlap(self, other: Tuple[Coord, Coord]) -> Optional[Tuple["Coord", "Coord"]]:
        ranges = [self.overlap_1d(other, i) for i in range(3)]
        if any(r is None for r in ranges):  # If no overlap, return None
            return None
        return tuple(Coord(*(ranges[d][i] for d in (0, 1, 2))) for i in (0, 1))

    def num_lit(self):
        if not self.on:
            return 0
        return self.c1.volume(self.c2)


def part1(cubes: List[Cube]) -> int:
    grid = set()
    for c in cubes:
        c.modify_grid(grid)
    return len(grid)


def part2_bad_explosion(cubes: List[Cube]) -> int:
    known_squares = []
    for cube in cubes:
        print(len(known_squares))
        new_known_squares = []
        for known in known_squares:
            for section in known.yield_non_overlap(cube):
                new_known_squares.append(section)
        if cube.on:
            new_known_squares.append(cube)
        known_squares = new_known_squares
    return sum(sq.num_lit() for sq in known_squares)


def part2(cubes: List[Cube]) -> int:
    seen_cubes: Dict[Tuple[Coord, Coord], int] = defaultdict(int)
    for cube in cubes:
        for sq, count in tuple(seen_cubes.items()):
            overlap = cube.overlap(sq)
            if overlap:
                seen_cubes[overlap] -= count
        if cube.on:
            seen_cubes[cube.c1, cube.c2] += 1
    return sum(c1.volume(c2) * count for (c1, c2), count in seen_cubes.items())


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    CUBES = [Cube.from_str(line) for line in DATA.split("\n")]
    print(part1(CUBES))
    print(part2(CUBES))
