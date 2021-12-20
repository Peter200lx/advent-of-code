from collections import Counter
from dataclasses import dataclass, field
from itertools import combinations, product, permutations
from pathlib import Path
from typing import List, NamedTuple, Dict, Tuple, Set

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int
    z: int

    def manhattan(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y, self.z - other.z)


class Transf(NamedTuple):
    first: Tuple[int, str]
    second: Tuple[int, str]
    third: Tuple[int, str]

    def mutate(self, coord: Coord):
        return Coord(
            self.first[0] * getattr(coord, self.first[1]),
            self.second[0] * getattr(coord, self.second[1]),
            self.third[0] * getattr(coord, self.third[1]),
        )

    @staticmethod
    def from_str(*transformation: str):
        assert len(transformation) == 3
        return Transf(*((1 if len(s) == 1 else -1, s[-1]) for s in transformation))


class FullConversion(NamedTuple):
    transf: Transf
    shift: Coord


ROTATIONS = [
    Transf(
        (X_muls[0], X_perm[0]),
        (X_muls[1], X_perm[1]),
        (X_muls[2], X_perm[2]),
    )
    for X_muls in product([-1, 1], [-1, 1], [-1, 1])
    for X_perm in permutations(["x", "y", "z"])
]


@dataclass
class Scanner:
    number: int
    seen_points: List[Coord] = field(repr=False)
    orientation_from_0: List[FullConversion] = field(default_factory=list)
    point_deltas: Dict[Coord, Tuple[Coord, Coord]] = field(init=False, repr=False)
    transformation_deltas: Dict[Coord, Tuple[Transf, Coord]] = field(
        default=None, repr=False
    )

    def corrected_location(self):
        if not self.orientation_from_0:
            return Coord(0, 0, 0)
        last, *rest = reversed(self.orientation_from_0)
        orientation = last.shift
        for conv in rest:
            orientation = conv.transf.mutate(orientation) + conv.shift
        return orientation

    def corrected_points(self) -> Set[Coord]:
        assert self.orientation_from_0, "Only should be called on scanners > 0"
        points = set(self.seen_points)
        for conv in reversed(self.orientation_from_0):
            points = {conv.transf.mutate(p) - conv.shift for p in points}
        return points

    def find_relative(self, other: "Scanner") -> bool:
        if not self.transformation_deltas:
            self.build_transformation_deltas()
        overlapping_deltas = (
            other.point_deltas.keys() & self.transformation_deltas.keys()
        )
        if len(overlapping_deltas) >= 12:
            overlap_transform_counter = Counter(
                self.transformation_deltas[k][0] for k in overlapping_deltas
            )
            for rel_transf, count in overlap_transform_counter.most_common():
                if count < 12:
                    continue
                an_overlap = next(
                    od
                    for od in overlapping_deltas
                    if self.transformation_deltas[od][0] == rel_transf
                )
                other_p1, other_p2 = other.point_deltas[an_overlap]
                my_p1, my_p2 = self.point_deltas[
                    self.transformation_deltas[an_overlap][1]
                ]
                point_delta = rel_transf.mutate(my_p1) - other_p1
                assert rel_transf.mutate(my_p2) - other_p2 == point_delta
                transformed_points = {
                    rel_transf.mutate(p) - point_delta for p in self.seen_points
                }
                if len(set(other.seen_points) & transformed_points) < 12:
                    continue
                self.orientation_from_0 = other.orientation_from_0 + [
                    FullConversion(rel_transf, point_delta)
                ]
                return True

    def build_point_deltas(self):
        self.point_deltas = {
            p1 - p2: (p1, p2) for p1, p2 in combinations(self.seen_points, 2)
        }

    def build_transformation_deltas(self):
        self.transformation_deltas = {
            t.mutate(p): (t, p) for t in ROTATIONS for p in self.point_deltas
        }

    @staticmethod
    def from_str(scanner_lines: str) -> "Scanner":
        name, *grids = scanner_lines.split("\n")
        number = int(name.split()[2])
        points = [
            Coord(int(x), int(y), int(z))
            for line in grids
            for x, y, z in [line.split(",")]
        ]
        s = Scanner(number, points)
        s.build_point_deltas()
        return s


def solve(scanners: List[Scanner]) -> Tuple[int, int]:
    scanner0, *unincorporated_scanners = scanners
    points = set(scanner0.seen_points)
    known_scanners = [scanner0]
    while known_scanners:
        first = known_scanners.pop()
        to_drop = []
        for i, second in enumerate(unincorporated_scanners):
            if second.find_relative(first):
                to_drop.append(i)
                second_points = second.corrected_points()
                assert len(points & second_points) >= 12
                points |= second_points
                known_scanners.append(second)
        for i in reversed(to_drop):
            del unincorporated_scanners[i]
    scanner_locations = {s.corrected_location() for s in scanners}
    return len(points), max(
        l1.manhattan(l2) for l1, l2 in combinations(scanner_locations, 2)
    )


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    SCANNERS = [Scanner.from_str(scan) for scan in DATA.split("\n\n")]

    print(solve(SCANNERS))
