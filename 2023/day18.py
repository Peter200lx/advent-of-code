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
        self.p1_walls = [cur]
        self.p2_walls = [p2_cur]
        for dir_str, length, color in insts:
            cur += DIRS[dir_str] * length
            self.p1_walls.append(cur)
            p2_length = int(color[:5], 16)
            p2_cur += HEX_DIRS[color[5]] * p2_length
            self.p2_walls.append(p2_cur)

    def total_dug(self, p2: bool = False):
        # https://www.101computing.net/the-shoelace-algorithm/
        walls = self.p2_walls if p2 else self.p1_walls
        lace1 = lace2 = 0
        wall_count = 0
        for i in range(1, len(walls)):
            lace1 += walls[i - 1].x * walls[i].y
            lace2 += walls[i - 1].y * walls[i].x
            if walls[i - 1].x == walls[i].x:
                wall_count += abs(walls[i - 1].y - walls[i].y)
            else:
                wall_count += abs(walls[i - 1].x - walls[i].x)
        lace1 += walls[-1].x * walls[0].y
        lace2 += walls[-1].y * walls[0].x

        return abs(lace1 - lace2) // 2 + wall_count // 2 + 1


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    DIGS_INSTS = [
        (d, int(n), c.strip("(#)")) for line in DATA.split("\n") for d, n, c in [line.split()]
    ]

    DIGSITE = Dig(DIGS_INSTS)

    print(DIGSITE.total_dug())

    print(DIGSITE.total_dug(p2=True))
