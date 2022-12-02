from pathlib import Path
from typing import List, Tuple

INPUT_FILE = Path(__file__).with_suffix(".input")

TYPE = {
    "A": 1,
    "B": 2,
    "C": 3,
    "X": 1,
    "Y": 2,
    "Z": 3,
}

CYCLE = {
    1: 2,
    2: 3,
    3: 1,
}

LOSS = 0
DRAW = 3
WIN = 6


def part1(strat: List[Tuple[str, str]]):
    total = 0
    for game in strat:
        opp, me = TYPE[game[0]], TYPE[game[1]]
        if opp == me:
            res = DRAW + me
        elif CYCLE[opp] == me:
            res = WIN + me
        else:
            res = LOSS + me
        total += res
    return total


def part2(strat: List[Tuple[str, str]]):
    total = 0
    for game in strat:
        opp, me = TYPE[game[0]], TYPE[game[1]]
        if game[1] == "Y":
            res = DRAW + opp
        elif game[1] == "Z":
            res = WIN + CYCLE[opp]
        else:
            res = LOSS + CYCLE[CYCLE[opp]]
        total += res
    return total


def top_n_sum(e):
    return e


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT_ELVES = [tuple(c for c in line.split()) for line in DATA.split("\n")]

    print(part1(INPUT_ELVES))
    print(part2(INPUT_ELVES))
