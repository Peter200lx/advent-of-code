from itertools import combinations
from pathlib import Path
from typing import NamedTuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y)


class Resonance:
    def __init__(self, data: str):
        self.antennas = {}
        lines = data.split("\n")
        self.size = Coord(len(lines[0]), len(lines))
        for y, line in enumerate(data.split("\n")):
            for x, c in enumerate(line):
                if c != ".":
                    tune_cloud = self.antennas.setdefault(c, set())
                    tune_cloud.add(Coord(x, y))

    def printg(self):
        for y in range(self.size.y):
            line = ""
            for x in range(self.size.x):
                loc = (x, y)
                for c, pcloud in self.antennas.items():
                    if loc in pcloud:
                        line += c
                        break
                else:
                    line += "."
            print(line)

    def p1(self) -> int:
        antinodes = set()
        for c, pcloud in self.antennas.items():
            for p1, p2 in combinations(pcloud, 2):
                for a in (p1 + p1 - p2, p2 + p2 - p1):
                    if 0 <= a.x < self.size.x and 0 <= a.y < self.size.y:
                        antinodes.add(a)
        return len(antinodes)

    def p2(self) -> int:
        antinodes = set()
        for c, pcloud in self.antennas.items():
            for p1, p2 in combinations(pcloud, 2):
                for a, d in ((p1, p1 - p2), (p2, p2 - p1)):
                    while 0 <= a.x < self.size.x and 0 <= a.y < self.size.y:
                        antinodes.add(a)
                        a += d
        return len(antinodes)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    FIELD = Resonance(DATA)

    print(FIELD.p1())
    print(FIELD.p2())
