import re
from pathlib import Path
from typing import NamedTuple

INPUT_FILE = Path(__file__).with_suffix(".input")

RE_NUMS = re.compile(r"-?\d+")

COSTS = {"A": 3, "B": 1}
P2_ADD = 10000000000000


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)

    def add_int(self, val):
        return Coord(self.x + val, self.y + val)


class NoMatch(Exception):
    pass


def inverse_algebra(b_a: Coord, b_b: Coord, result: Coord) -> tuple[int, int]:
    # https://en.wikipedia.org/wiki/Cramer%27s_rule#Explicit_formulas_for_small_systems
    a = (result.x * b_b.y - b_b.x * result.y) / (b_a.x * b_b.y - b_b.x * b_a.y)
    if not a.is_integer():
        raise NoMatch
    b = (b_a.x * result.y - result.x * b_a.y) / (b_a.x * b_b.y - b_b.x * b_a.y)
    if not b.is_integer():
        raise NoMatch
    return int(a), int(b)


class Machine:
    def __init__(self, data: str):
        a_str, b_str, prize_str = data.split("\n")
        self.buttons = {}
        for button_str in (a_str, b_str):
            char_str, coords = button_str.split(": ")
            self.buttons[char_str[-1]] = Coord(*map(int, RE_NUMS.findall(coords)))
        self.prize = Coord(*map(int, RE_NUMS.findall(prize_str)))

    def __repr__(self):
        return f"Machine({self.buttons=}, {self.prize=})"

    def cheapest_path(self, p2=False) -> int:
        prize = self.prize if not p2 else self.prize.add_int(P2_ADD)
        try:
            a, b = inverse_algebra(*self.buttons.values(), result=prize)
        except NoMatch:
            return False
        if not p2:
            for v in (a, b):
                if not 0 <= v < 100:
                    return False
        return COSTS["A"] * a + COSTS["B"] * b


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    MACHINES = [Machine(chunk) for chunk in DATA.split("\n\n")]

    print(sum(m.cheapest_path() for m in MACHINES))
    print(sum(m.cheapest_path(p2=True) for m in MACHINES))
