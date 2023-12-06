import re
from math import prod
from pathlib import Path
from typing import List

INPUT_FILE = Path(__file__).with_suffix(".input")

RE_NUMS = re.compile(r"-?\d+")


class Race:
    def __init__(self, time: int, dist: int):
        self.time = time
        self.dist = dist

    def __repr__(self):
        return f"Race({self.time}, {self.dist=})"

    def run_race(self, hold: int) -> int:
        speed = hold
        remaining = self.time - hold
        return speed * remaining


def parse_input(instr: str) -> List[Race]:
    tstr, dstr = instr.split("\n")
    times = list(map(int, RE_NUMS.findall(tstr)))
    dists = list(map(int, RE_NUMS.findall(dstr)))
    assert len(times) == len(dists)
    return [Race(t, d) for t, d in zip(times, dists)]


def solve(instr: str):
    races = parse_input(instr)
    ways = []
    for n, race in enumerate(races):
        wins = 0
        for i in range(1, race.time):
            dist = race.run_race(i)
            if dist > race.dist:
                wins += 1
        ways.append(wins)
    return prod(ways)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    print(solve(DATA))

    print(solve(DATA.replace(" ", "")))
