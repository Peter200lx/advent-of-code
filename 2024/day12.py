from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import NamedTuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)


# fmt: off
DIRS = [              Coord(0, -1),
        Coord(-1, 0),                Coord(1, 0),
                      Coord(0, 1),]
# fmt: on


class Plot(NamedTuple):
    inside: dict[Coord, set[Coord]]
    adjacent: dict[Coord, set[Coord]]

    @classmethod
    def make(cls, field: dict[Coord, str], start: Coord) -> "Plot":
        inside = {}
        adjacent = defaultdict(set)
        possible = {start}
        my_letter = field[start]
        while possible:
            coord = possible.pop()
            inside[coord] = set()
            for d in DIRS:
                new_loc = coord + d
                if field.get(new_loc) == my_letter:
                    if new_loc not in inside:
                        possible.add(new_loc)
                else:
                    inside[coord].add(d)
                    adjacent[new_loc].add(d)
        return cls(inside, adjacent)

    @property
    def sides_old(self):
        dir_groupings: dict[Coord, list[set[Coord]]] = {d: [] for d in DIRS}
        for coord in self.adjacent:
            found = set()
            for d in DIRS:
                new_loc = coord + d
                if new_loc in self.adjacent:
                    shared_dirs = self.adjacent[coord] & self.adjacent[new_loc]
                    for dir in shared_dirs:
                        found.add(dir)
                        my_side = {coord, new_loc}
                        for side in dir_groupings[dir]:
                            if side & my_side:  # Any shared points
                                side |= my_side  # add other point to set
                                break
                        else:
                            dir_groupings[dir].append(my_side)
            for dir_remain in self.adjacent[coord] - found:
                dir_groupings[dir_remain].append(set())
        return sum(len(rs) for rs in dir_groupings.values())

    @property
    def sides(self):
        c_d_groupings = []
        for coord, dir_set in self.inside.items():
            if not dir_set:  # if nothing adjacent to outside
                continue
            found = set()
            for new_loc in (coord + d for d in DIRS):
                for direc in dir_set & self.inside.get(new_loc, set()):
                    found.add(direc)
                    my_side = {(coord, direc), (new_loc, direc)}
                    for side in c_d_groupings:
                        if side & my_side:  # Any shared points
                            side |= my_side  # add other point to set
                            break
                    else:
                        c_d_groupings.append(my_side)
            for dir_remain in dir_set - found:
                c_d_groupings.append({(coord, dir_remain)})
        to_many = 0
        for a, b in combinations(c_d_groupings, 2):
            if a & b:
                to_many += 1
        return len(c_d_groupings) - to_many


class Map:
    def __init__(self, data: str):
        self.locs = {}
        lines = data.split("\n")
        self.size = Coord(len(lines[0]), len(lines))
        self.plots: dict[str, list[Plot]] = {}
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                self.locs[Coord(x, y)] = c
        seen = set()
        for coord in self.locs:
            if coord in seen:
                continue
            letter_plots = self.plots.setdefault(self.locs[coord], [])
            letter_plots.append(Plot.make(self.locs, coord))
            seen |= letter_plots[-1].inside.keys()

    def printg(self):
        for y in range(self.size.y):
            print("".join(f"{self.locs[(x, y)]}" for x in range(self.size.x)))

    def p1(self) -> int:
        return sum(
            len(p.inside) * sum(len(a) for a in p.inside.values())
            for plot in self.plots.values()
            for p in plot
        )

    def p2(self) -> int:
        return sum(
            len(p.inside) * p.sides for plot in self.plots.values() for p in plot
        )


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    MAP = Map(DATA)

    print(MAP.p1())
    print(MAP.p2())
