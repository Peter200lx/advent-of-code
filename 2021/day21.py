from collections import Counter
from itertools import islice
from pathlib import Path
from typing import List, Tuple, Iterator

INPUT_FILE = Path(__file__).with_suffix(".input")

DNUMS = (1, 2, 3)
DIRAC_DIE = Counter(
    r1 + r2 + r3 for r1 in DNUMS for r2 in DNUMS for r3 in DNUMS
).most_common()


def det_die() -> Iterator[int]:
    while True:
        yield from range(1, 101)


def part1(player_positions: List[int]) -> int:
    player_positions = [n - 1 for n in player_positions]
    player_scores = [0, 0]
    player = rolls = 0
    determ_die = det_die()
    while all(sc < 1000 for sc in player_scores):
        roll = sum(islice(determ_die, 3))
        rolls += 3
        move = (player_positions[player] + roll) % 10
        player_scores[player] += move + 1
        player_positions[player] = move
        player = (player + 1) % 2
    return rolls * min(player_scores)


def part2(pos: Tuple[int, int], sco: Tuple[int, int], seen: dict) -> Tuple[int, int]:
    if prior := seen.get((pos, sco)):
        return prior
    if sco[0] >= 21:
        assert sco[1] < 21
        return 1, 0
    elif sco[1] >= 21:
        return 0, 1
    wins = (0, 0)
    for roll, roll_count in DIRAC_DIE:
        move = (pos[0] + roll) % 10
        p2w, p1w = part2((pos[1], move), (sco[1], sco[0] + move + 1), seen)
        wins = (wins[0] + p1w * roll_count, wins[1] + p2w * roll_count)
    seen[(pos, sco)] = wins
    return wins


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    START = [int(n) for line in DATA.split("\n") for *_, n in [line.split()]]
    print(part1(START))
    print(max(part2((START[0] - 1, START[1] - 1), (0, 0), {})))
