from collections import Counter
from pathlib import Path
from typing import Tuple

INPUT_FILE = Path(__file__).with_suffix(".input")

CARDS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
CARDS_P2 = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]

TYPES = ["5", "4", "F", "3", "2P", "1P", "H"]


class Hand:
    def __init__(self, line: str):
        cards, bid = line.split()
        self.cards = cards
        self.bid = int(bid)
        self.value = self.make_val(cards)
        if "J" not in cards:
            self.p2_type = self.make_val(cards)
        else:
            possible_types = []
            for c in cards:
                if c != "J":
                    possible_types.append(self.make_val(cards.replace("J", c)))
            if not possible_types:
                self.p2_type = "5"
            else:
                self.p2_type = min(possible_types, key=lambda x: TYPES.index(x[0]))
        self.p2_mode = False

    @staticmethod
    def make_val(cards: str) -> Tuple[str, str]:
        cards = Counter(cards)
        if len(cards) == 1:
            most, _count = cards.most_common()[0]
            return ("5", most)
        elif len(cards) == 2:
            (most, count), (least, _single) = cards.most_common()
            if count == 4:
                return ("4", most)
            elif count == 3:
                return ("F", most)
        elif len(cards) == 3:
            (most, count), (mid, mcount), (least, lcount) = cards.most_common()
            if count == 3:
                return ("3", most)
            if count == 2:
                assert mcount == 2
                return ("2P", min(most, mid, key=lambda x: CARDS.index(x)))
        elif len(cards) == 4:
            (most, count) = cards.most_common(1)[0]
            assert count == 2
            return ("1P", most)
        else:
            return ("H", min(cards.keys(), key=lambda x: CARDS.index(x)))

    def __repr__(self):
        return f"Hand({self.cards}, {self.bid=} {self.value=})"

    def __lt__(self, other: "Hand"):
        my_type = self.p2_type[0] if self.p2_mode else self.value[0]
        other_type = other.p2_type[0] if self.p2_mode else other.value[0]
        if TYPES.index(my_type) < TYPES.index(other_type):
            return True
        if my_type == other_type:
            order = CARDS_P2 if self.p2_mode else CARDS
            for i, my_card in enumerate(self.cards):
                if order.index(my_card) < order.index(other.cards[i]):
                    return True
                elif order.index(my_card) > order.index(other.cards[i]):
                    return False
        return False

    def __eq__(self, other):
        return self.value == other.value


def solve(hands):
    hands = list(hands)
    hands.sort(reverse=True)
    return sum(h.bid * i for i, h in enumerate(hands, start=1))


def part_two(hands):
    for h in hands:
        h.p2_mode = True
    hands.sort(reverse=True)
    return sum(h.bid * i for i, h in enumerate(hands, start=1))


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    HANDS = [Hand(line) for line in DATA.split("\n")]

    print(solve(HANDS))
    print(part_two(HANDS))
