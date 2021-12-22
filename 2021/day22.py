import re
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple, Dict, List, Optional, Tuple

INPUT_FILE = Path(__file__).with_suffix(".input")

RE_NUMS = re.compile(r"-?\d+")


class Coord(NamedTuple):
    x: int
    y: int
    z: int

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

    def overlap_1d(
        self, other: Tuple[Coord, Coord], dimension: int
    ) -> Optional[Tuple[int, int]]:
        my_min, my_max = self.c1[dimension], self.c2[dimension]
        o_min, o_max = other[0][dimension], other[1][dimension]
        if o_min > my_max or my_min > o_max:
            return None  # no overlap
        return max(o_min, my_min), min(o_max, my_max)

    def overlap(self, other: Tuple[Coord, Coord]) -> Optional[Tuple["Coord", "Coord"]]:
        if (
            (xr := self.overlap_1d(other, 0)) is None
            or (yr := self.overlap_1d(other, 1)) is None
            or (zr := self.overlap_1d(other, 2)) is None
        ):
            return None
        return tuple(Coord(xr[i], yr[i], zr[i]) for i in (0, 1))


def part1(cubes: List[Cube]) -> int:
    max_space = Cube(False, Coord(-50, -50, -50), Coord(50, 50, 50))
    seen_cubes: Dict[Tuple[Coord, Coord], int] = defaultdict(int)
    for cube in cubes:
        if max_overlap := max_space.overlap((cube.c1, cube.c2)):
            for sq, count in tuple(seen_cubes.items()):
                if overlap := cube.overlap(sq):
                    seen_cubes[overlap] -= count
            if cube.on:
                seen_cubes[max_overlap] += 1
    return sum(c1.volume(c2) * count for (c1, c2), count in seen_cubes.items())


def part2(cubes: List[Cube]) -> int:
    seen_cubes: Dict[Tuple[Coord, Coord], int] = defaultdict(int)
    for cube in cubes:
        for sq, count in tuple(seen_cubes.items()):
            if count == 0:
                del seen_cubes[sq]
                continue
            if overlap := cube.overlap(sq):
                seen_cubes[overlap] -= count
        if cube.on:
            seen_cubes[cube.c1, cube.c2] += 1
    return sum(c1.volume(c2) * count for (c1, c2), count in seen_cubes.items())


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    CUBES = [Cube.from_str(line) for line in DATA.split("\n")]
    print(part1(CUBES))
    print(part2(CUBES))
