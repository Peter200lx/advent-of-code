from pathlib import Path
from typing import List, Set, Tuple

FILE_DIR = Path(__file__).parent


def play_game(p1: List[int], p2: List[int]):
    while p1 and p2:
        p1_card, p2_card = p1.pop(0), p2.pop(0)
        if p1_card > p2_card:
            p1 += [p1_card, p2_card]
        elif p2_card > p1_card:
            p2 += [p2_card, p1_card]
        else:
            raise Exception
    victor_deck = p1 or p2
    return sum(i * c for i, c in enumerate(reversed(victor_deck), start=1))


def play_recursive_game(p1: Tuple[int], p2: Tuple[int]):
    previous_rounds: Set[Tuple[Tuple[int, ...], Tuple[int, ...]]] = set()
    while p1 and p2:
        if (p1, p2) in previous_rounds:  # Recursion prevention
            return p1, tuple()
        previous_rounds.add((p1, p2))
        p1_card, p2_card = p1[0], p2[0]
        p1, p2 = p1[1:], p2[1:]
        if p1_card <= len(p1) and p2_card <= len(p2):
            win_result = play_recursive_game(p1[:p1_card], p2[:p2_card])
            if win_result[0]:
                p1 += (p1_card, p2_card)
            else:
                p2 += (p2_card, p1_card)
        else:
            if p1_card > p2_card:
                p1 += (p1_card, p2_card)
            else:
                p2 += (p2_card, p1_card)
    return p1, p2


if __name__ == "__main__":
    DATA = (FILE_DIR / "day22.input").read_text().strip()
    P1STR, P2STR = DATA.split("\n\n")
    P1, P2 = tuple(int(s) for s in P1STR.split("\n")[1:]), tuple(int(s) for s in P2STR.split("\n")[1:])
    print(play_game(list(P1), list(P2)))
    recursive_result = play_recursive_game(tuple(P1), tuple(P2))
    recursive_winner = recursive_result[0] or recursive_result[1]
    print(sum(i * c for i, c in enumerate(reversed(recursive_winner), start=1)))
