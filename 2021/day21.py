from itertools import islice
from pathlib import Path
from typing import List, Tuple

INPUT_FILE = Path(__file__).with_suffix(".input")


def det_die():
    while True:
        yield from range(1, 101)


def dir_die():
    nums = (1, 2, 3)
    yield from (r1 + r2 + r3 for r1 in nums for r2 in nums for r3 in nums)


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


def part2(
    player: int, pos: Tuple[int, int], sco: Tuple[int, int], seen: dict
) -> Tuple[int, int]:
    if prior := seen.get((player, pos, sco)):
        return prior
    if sco[0] >= 21:
        assert sco[1] < 21
        return 1, 0
    elif sco[1] >= 21:
        return 0, 1
    wins = [0, 0]
    for roll in dir_die():
        move = (pos[player] + roll) % 10
        if player:
            new_wins = part2(0, (pos[0], move), (sco[0], sco[1] + move + 1), seen)
        else:
            new_wins = part2(1, (move, pos[1]), (sco[0] + move + 1, sco[1]), seen)
        wins = [wins[0] + new_wins[0], wins[1] + new_wins[1]]
    seen[(player, pos, sco)] = wins
    return wins


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    START = [int(n) for line in DATA.split("\n") for *_, n in [line.split()]]
    print(part1(START))
    print(max(part2(0, (START[0] - 1, START[1] - 1), (0, 0), {})))
