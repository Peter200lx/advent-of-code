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


def p1(coords: set[Coord], limit: int) -> int:
    junctions = {}
    combs = sorted(
        (first.dist(second), first, second) for first, second in combinations(coords, 2)
    )
    performed = 0
    for _dist, first, second in combs:
        first_set = junctions.setdefault(first, set())
        second_set = junctions.setdefault(second, set())
        final_set = {first, second}
        if first_set and second_set:
            final_set |= first_set | second_set
        elif first_set:
            final_set |= first_set
        elif second_set:
            final_set |= second_set
        for loc in final_set:
            junctions[loc] = final_set
        performed += 1
        if performed >= limit:
            break
    unique_sets = []
    for junction in junctions.values():
        if junction not in unique_sets:
            unique_sets.append(junction)
    return prod(sorted([len(j) for j in unique_sets], reverse=True)[:3])


def p2(coords: set[Coord]) -> int:
    junctions = {}
    combs = [
        (first.dist(second), first, second) for first, second in combinations(coords, 2)
    ]
    combs.sort()
    for _dist, first, second in combs:
        first_set = junctions.setdefault(first, set())
        second_set = junctions.setdefault(second, set())
        final_set = {first, second}
        if first_set and second_set:
            final_set |= first_set | second_set
        elif first_set:
            final_set |= first_set
        elif second_set:
            final_set |= second_set
        if len(final_set) == len(coords):
            return first.x * second.x
        for loc in final_set:
            junctions[loc] = final_set


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    FIELD = {
        Coord(int(x), int(y), int(z))
        for line in DATA.split("\n")
        for x, y, z in [line.split(",")]
    }

    print((p1(FIELD, P1_PAIRS)))
    print((p2(FIELD)))
