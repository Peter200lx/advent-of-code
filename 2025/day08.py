from itertools import combinations
from math import sqrt, prod
from pathlib import Path
from typing import NamedTuple

INPUT_FILE = Path(__file__).with_suffix(".input")

P1_PAIRS = 1000


class Coord(NamedTuple):
    x: int
    y: int
    z: int

    def dist(self, other: "Coord") -> float:
        return sqrt(
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        )


def solve(coords: set[Coord], limit: int) -> tuple[int, int]:
    part1 = None
    junctions = {}
    combs = sorted(
        (first.dist(second), first, second) for first, second in combinations(coords, 2)
    )
    performed = 0
    for _dist, first, second in combs:
        first_set = junctions.setdefault(first, set())
        second_set = junctions.setdefault(second, set())
        final_set = {first, second}
        final_set |= first_set | second_set

        if len(final_set) == len(coords):
            return part1, first.x * second.x

        for loc in final_set:
            junctions[loc] = final_set

        performed += 1
        if performed == limit:
            unique_sets = []
            for junction in junctions.values():
                if junction not in unique_sets:
                    unique_sets.append(junction)
            part1 = prod(sorted([len(j) for j in unique_sets], reverse=True)[:3])


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    FIELD = {
        Coord(int(x), int(y), int(z))
        for line in DATA.split("\n")
        for x, y, z in [line.split(",")]
    }

    print("\n".join(str(n) for n in solve(FIELD, P1_PAIRS)))
