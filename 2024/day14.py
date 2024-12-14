import re
from collections import Counter
from pathlib import Path
from typing import NamedTuple

INPUT_FILE = Path(__file__).with_suffix(".input")

RE_NUMS = re.compile(r"-?\d+")


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)

    def __mod__(self, other) -> "Coord":
        return Coord(self.x % other.x, self.y % other.y)


P1_SPACE = Coord(101, 103)
P1_LOOPS = 100


class Robot(NamedTuple):
    point: Coord
    vel: Coord

    @classmethod
    def make(cls, line: str):
        p, v = line.split()
        return cls(
            Coord(*map(int, RE_NUMS.findall(p))), Coord(*map(int, RE_NUMS.findall(v)))
        )

    def __repr__(self):
        return f"Robot({self.p=}, {self.v=})"

    def step(self):
        return Robot((self.point + self.vel) % P1_SPACE, self.vel)


def printg(robots: dict[Coord, int]):
    for y in range(P1_SPACE.y):
        print(
            "".join(
                f"{robots[(x,y)]}" if (x, y) in robots else "."
                for x in range(P1_SPACE.x)
            )
        )


def p1(robots: list[Robot]) -> int:
    robots = list(robots)
    for i in range(P1_LOOPS):
        robots = [r.step() for r in robots]
    mid_x = P1_SPACE.x // 2
    mid_y = P1_SPACE.y // 2
    res = 1
    for x_range, y_range in (
        (range(0, mid_x), range(0, mid_y)),
        (range(0, mid_x), range(mid_y + 1, P1_SPACE.y)),
        (range(mid_x + 1, P1_SPACE.x), range(0, mid_y)),
        (range(mid_x + 1, P1_SPACE.x), range(mid_y + 1, P1_SPACE.y)),
    ):
        cnt = sum(1 for r in robots if r.point.x in x_range and r.point.y in y_range)
        res *= cnt
    return res


def p2_print(robots: list[Robot]) -> int:
    # mid_x = P1_SPACE.x // 2
    for i in range(500):
        robots = [r.step() for r in robots]
        printg(dict(Counter(r.point for r in robots)))
        print(i + 1)

        # valid = True
        # for y in range(0, 4):
        #     x_ranges = (range(0, mid_x-y), range(mid_x+1+y, P1_SPACE.x))
        #     for x_range in x_ranges:
        #         if any(r.point.x in x_range and r.point.y == y for r in robots):
        #             valid = False
        #             break
        #     if not valid:
        #         break
        # if valid:
        #     printg(dict(Counter(r.point for r in robots)))
        #     print(i)
        #     break


def p2():
    x = 14  # vertical pattern found
    y = 64  # horizontal pattern found
    while x != y:
        if x < y:
            x += P1_SPACE.x
        elif x > y:
            y += P1_SPACE.y
    return x


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    ROBOTS = [Robot.make(line) for line in DATA.split("\n")]

    print(p1(ROBOTS))
    # p2_print(ROBOTS)
    print(p2())
