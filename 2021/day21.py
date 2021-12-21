from itertools import islice
from typing import List, Tuple


def det_die():
    i = 1
    while True:
        yield i
        i += 1
        if i > 100:
            i = 1


def dir_die():
    for r1 in (1, 2, 3):
        for r2 in (1, 2, 3):
            for r3 in (1, 2, 3):
                yield r1 + r2 + r3


def part1(player_positions: List[int]) -> int:
    player_positions = [player_positions[0] - 1, player_positions[1] - 1]
    player_scores = [0, 0]
    player = 0
    determ_die = det_die()
    rolls = 0
    while all(sc < 1000 for sc in player_scores):
        move = sum(islice(determ_die, 3))
        rolls += 3
        new_position = (player_positions[player] + move) % 10
        player_scores[player] += new_position + 1
        player_positions[player] = new_position
        player = (player + 1) % 2
    return rolls * min(player_scores)


def part2(
    player: int, pos: Tuple[int, int], sco: Tuple[int, int], seen: dict
) -> Tuple[int, int]:
    prior = seen.get((player, pos, sco))
    if prior:
        return prior
    if sco[0] >= 21:
        assert sco[1] < 21
        return 1, 0
    elif sco[1] >= 21:
        return 0, 1
    p1wins = p2wins = 0
    for roll in dir_die():
        move = (pos[player] + roll) % 10
        if player:
            np1wins, np2wins = part2(
                (player + 1) % 2, (pos[0], move), (sco[0], sco[1] + move + 1), seen
            )
        else:
            np1wins, np2wins = part2(
                (player + 1) % 2, (move, pos[1]), (sco[0] + move + 1, sco[1]), seen
            )
        p1wins += np1wins
        p2wins += np2wins
    seen[(player, pos, sco)] = p1wins, p2wins
    return p1wins, p2wins


if __name__ == "__main__":
    START = [1, 2]  # My Input   | 1, 2
    # START = [4, 8]  # Test Input | 4, 8
    print(part1(START))
    print(max(part2(0, (START[0] - 1, START[1] - 1), (0, 0), {})))
