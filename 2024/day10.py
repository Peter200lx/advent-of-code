from pathlib import Path
from typing import NamedTuple, Optional

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y)


# fmt: off
P1_D = [              Coord(0, -1),
        Coord(-1, 0),                Coord(1, 0),
                      Coord(0, 1),]
# fmt: on


class Map:
    def __init__(self, data: str):
        self.locs = {}
        self.p1_starts = set()
        lines = data.split("\n")
        self.size = Coord(len(lines[0]), len(lines))
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == "0":
                    self.p1_starts.add(Coord(x, y))
                self.locs[Coord(x, y)] = int(c)

    def printg(self):
        for y in range(self.size.y):
            print("".join(f"{self.locs[(x, y)]}" for x in range(self.size.x)))

    def score(self, cur: Coord, seen_locs: Optional[set[Coord]]) -> int:
        cur_val = self.locs[cur]
        if isinstance(seen_locs, set):
            if cur in seen_locs:
                return 0
        if cur_val == 9:
            if isinstance(seen_locs, set):
                seen_locs.add(cur)
            return 1
        ret = 0
        for d in P1_D:
            next_loc = cur + d
            next_val = self.locs.get(next_loc, -1)
            if next_val == cur_val + 1:
                ret += self.score(next_loc, seen_locs)
        return ret

    def p1(self) -> int:
        return sum(self.score(c, set()) for c in self.p1_starts)

    def p2(self) -> int:
        return sum(self.score(c, None) for c in self.p1_starts)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    MAP = Map(DATA)

    print(MAP.p1())
    print(MAP.p2())
