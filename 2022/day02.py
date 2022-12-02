from pathlib import Path

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


def part1(c1: str, c2: str) -> int:
    opp, me = TYPE[c1], TYPE[c2]
    if opp == me:
        return DRAW + me
    elif CYCLE[opp] == me:
        return WIN + me
    return LOSS + me


def part2(c1: str, c2: str) -> int:
    opp = TYPE[c1]
    if c2 == "Y":
        return DRAW + opp
    elif c2 == "Z":
        return WIN + CYCLE[opp]
    return LOSS + CYCLE[CYCLE[opp]]


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT_ELVES = [[c for c in line.split()] for line in DATA.split("\n")]

    print(sum(part1(r[0], r[1]) for r in INPUT_ELVES))
    print(sum(part2(r[0], r[1]) for r in INPUT_ELVES))
