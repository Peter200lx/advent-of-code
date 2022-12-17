from pathlib import Path
from typing import List, NamedTuple, Set, Optional, Iterable, Iterator

INPUT_FILE = Path(__file__).with_suffix(".input")

ROCKSTR = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##"""


class Pos(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Pos") -> "Pos":
        return Pos(self.x + other.x, self.y + other.y)


def parse_rocks(rocks_str: str) -> List[List[Pos]]:
    rocks = []
    for rock_str in rocks_str.split("\n\n"):
        rock = []
        height = len(rock_str.split("\n")) - 1
        for y, line in enumerate(rock_str.split("\n")):
            for x, c in enumerate(line):
                if c == "#":
                    rock.append(Pos(x, y - height))
        rocks.append(rock)
    return rocks


ROCKS = parse_rocks(ROCKSTR)
P1_ROCK_COUNT = 2022
P2_ROCK_COUNT = 1000000000000
WINDDIR = {"<": Pos(-1, 0), ">": Pos(1, 0)}
LEFT_DIST = 3
ABOVE = -4
DOWN_MOVE = Pos(0, 1)


def wind_gen(wind: str) -> Iterator[Pos]:
    while True:
        for c in wind:
            yield WINDDIR[c]


def rock_gen(rocks: List[List[Pos]]) -> Iterator[List[Pos]]:
    while True:
        yield from rocks


def print_column(locked_rocks: Set[Pos], cur_rock: List[Pos]):
    cur_rock = set(cur_rock)
    y_top = min(p.y for p in cur_rock)
    for y in range(y_top, 0):
        print(
            "|"
            + "".join(
                "@" if (x, y) in cur_rock else "#" if (x, y) in locked_rocks else "."
                for x in range(1, 8)
            )
            + "|"
        )
    print("+-------+")


def part_1(wind: str, rocks: List[List[Pos]], rock_count: int = P1_ROCK_COUNT):
    wind_iter = wind_gen(wind)
    rock_iter = rock_gen(rocks)
    locked_rocks: Set[Pos] = set()
    y_top = 0
    for i in range(rock_count):
        cur_rock = next(rock_iter)
        shift = Pos(LEFT_DIST, y_top + ABOVE)
        cur_rock = [p + shift for p in cur_rock]
        stopped = False
        while not stopped:
            # print_column(locked_rocks, cur_rock)
            wind_shift = next(wind_iter)
            # print(f"{wind_shift=}")
            try_rock = [p + wind_shift for p in cur_rock]
            if not any(p.x <= 0 or p.x > 7 or p in locked_rocks for p in try_rock):
                cur_rock = try_rock
            try_rock = [p + DOWN_MOVE for p in cur_rock]
            if not any(p.y >= 0 or p in locked_rocks for p in try_rock):
                cur_rock = try_rock
            else:
                y_top = min(y_top, min(p.y for p in cur_rock))
                locked_rocks |= set(cur_rock)
                stopped = True
    return -y_top


def part_2(wind: str, rocks: List[List[Pos]]):
    repeat_len = len(wind) * len(rocks)
    print(f"{len(wind)=}, {len(rocks)=}, {repeat_len=}")
    wind_iter = wind_gen(wind)
    rock_iter = rock_gen(rocks)
    locked_rocks: Set[Pos] = set()
    y_top = 0
    height_list = []
    checked_length = 1
    for i in range(P2_ROCK_COUNT):
        cur_rock = next(rock_iter)
        shift = Pos(LEFT_DIST, y_top + ABOVE)
        cur_rock = [p + shift for p in cur_rock]
        while True:
            wind_shift = next(wind_iter)
            try_rock = [p + wind_shift for p in cur_rock]
            if not any(p.x <= 0 or p.x > 7 or p in locked_rocks for p in try_rock):
                cur_rock = try_rock
            try_rock = [p + DOWN_MOVE for p in cur_rock]
            if not any(p.y >= 0 or p in locked_rocks for p in try_rock):
                cur_rock = try_rock
            else:
                y_top = min(y_top, min(p.y for p in cur_rock))
                height_list.append(-y_top)
                locked_rocks |= set(cur_rock)
                break
        if i % (5 * repeat_len) == 0:  # Clear out locked_rocks regularly
            locked_rocks = {p for p in locked_rocks if p.y < (y_top + 50)}
        if (
            i > (checked_length * 2 + 10) * repeat_len
            and i % (checked_length * repeat_len) == 0
        ):
            ranges = list(range(checked_length, 2 * checked_length + 1))
            print(f"Checking for repeats at {i} for {ranges}")
            inc_pattern = [
                height_list[i + 1] - height_list[i] for i in range(len(height_list) - 1)
            ]
            for j in ranges:
                if (
                    inc_pattern[-repeat_len * j :]
                    == inc_pattern[-repeat_len * j * 2 : -repeat_len * j]
                ):
                    print(f"Found repeat at {i} with repeat {j}")
                    repeat_amount = sum(inc_pattern[-repeat_len * j :])

                    remaining_i = P2_ROCK_COUNT - i
                    jump_count = remaining_i // (j * repeat_len)
                    y_top -= jump_count * repeat_amount
                    print(f"Jumping from {i=} to {i+jump_count * j * repeat_len}")
                    i += jump_count * j * repeat_len
                    remaining_i = P2_ROCK_COUNT - i
                    return -(
                        y_top
                        - sum(
                            inc_pattern[
                                -repeat_len * j : -repeat_len * j + remaining_i - 1
                            ]
                        )
                    )
                else:
                    checked_length = j
            print(f"Failed to find repeats")
    return y_top


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    WIND_MOVEMENTS = DATA

    print(part_1(WIND_MOVEMENTS, ROCKS))
    print(part_2(WIND_MOVEMENTS, ROCKS))
