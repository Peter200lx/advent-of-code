from pathlib import Path
from typing import List, NamedTuple, Tuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)

    def __mul__(self, num: int):
        return Coord(self.x * num, self.y * num)


ROTATIONS = {
    Coord(0, 1): [Coord(-1, 0), Coord(1, 0)],
    Coord(0, -1): [Coord(-1, 0), Coord(1, 0)],
    Coord(1, 0): [Coord(0, -1), Coord(0, 1)],
    Coord(-1, 0): [Coord(0, -1), Coord(0, 1)],
}


DIRS = {
    "R": Coord(1, 0),
    "L": Coord(-1, 0),
    "U": Coord(0, -1),
    "D": Coord(0, 1),
}

HEX_DIRS = {
    "0": DIRS["R"],
    "1": DIRS["D"],
    "2": DIRS["L"],
    "3": DIRS["U"],
}


class Dig:
    def __init__(self, insts: List[Tuple[str, int, str]]):
        cur = p2_cur = Coord(0, 0)
        self.walls = {}
        self.p2_walls = [p2_cur]
        for dir_str, length, color in insts:
            direct = DIRS[dir_str]
            for i in range(length):
                cur += direct
                self.walls[cur] = color
            p2_length = int(color[:5], 16)
            p2_cur += HEX_DIRS[color[5]] * p2_length
            self.p2_walls.append(p2_cur)

    def print(self):
        minx, maxx = min(c.x for c in self.walls), max(c.x for c in self.walls)
        miny, maxy = min(c.y for c in self.walls), max(c.y for c in self.walls)
        for y in range(miny, maxy + 1):
            print(
                "".join(
                    self.walls[(x, y)][0] if (x, y) in self.walls else "."
                    for x in range(minx, maxx + 1)
                )
            )

    def dug_amount(self):
        minx = min(c.x for c in self.walls)
        for point in (c for c in self.walls if c.x == minx):
            maybe_start = point + DIRS["R"]
            if maybe_start in self.walls:
                continue
            else:
                break
        dug = set()
        to_proc = [maybe_start]
        while to_proc:
            cur = to_proc.pop()
            for adj in DIRS.values():
                new_cur = cur + adj
                if new_cur in self.walls or new_cur in dug:
                    continue
                dug.add(new_cur)
                if new_cur not in to_proc:
                    to_proc.append(new_cur)
        return len(self.walls) + len(dug)

    def p2_dug_amount(self):
        # https://www.101computing.net/the-shoelace-algorithm/
        lace1 = lace2 = 0
        walls = 0
        for i in range(1, len(self.p2_walls)):
            lace1 += self.p2_walls[i - 1].x * self.p2_walls[i].y
            lace2 += self.p2_walls[i - 1].y * self.p2_walls[i].x
            if self.p2_walls[i - 1].x == self.p2_walls[i].x:
                walls += abs(self.p2_walls[i - 1].y - self.p2_walls[i].y)
            else:
                walls += abs(self.p2_walls[i - 1].x - self.p2_walls[i].x)
        lace1 += self.p2_walls[-1].x * self.p2_walls[0].y
        lace2 += self.p2_walls[-1].y * self.p2_walls[0].x

        return abs(lace1 - lace2) // 2 + walls // 2 + 1


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    DIGS_INSTS = [
        (d, int(n), c.strip("(#)")) for line in DATA.split("\n") for d, n, c in [line.split()]
    ]

    DIGSITE = Dig(DIGS_INSTS)

    print(DIGSITE.dug_amount())

    print(DIGSITE.p2_dug_amount())
