from collections import Counter
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

CARDS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
CARDS_P2 = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]

TYPES = ["5", "4", "F", "3", "2P", "1P", "H"]


def find_type(cards: str) -> str:
    cards = Counter(cards)
    _most, count = cards.most_common(1)[0]
    if len(cards) == 1:
        return "5"
    elif len(cards) == 2:
        if count == 4:
            return "4"
        elif count == 3:
            return "F"
    elif len(cards) == 3:
        if count == 3:
            return "3"
        if count == 2:
            return "2P"
    elif len(cards) == 4:
        return "1P"
    else:
        return "H"


class Hand:
    def __init__(self, line: str):
        cards, bid = line.split()
        self.cards = cards
        self.bid = int(bid)
        self.type = find_type(cards)
        self.card_order = CARDS

    def __lt__(self, other: "Hand"):
        if TYPES.index(self.type) > TYPES.index(other.type):
            return True
        if self.type == other.type:
            for i, my_card in enumerate(self.cards):
                if self.card_order.index(my_card) > self.card_order.index(other.cards[i]):
                    return True
                elif self.card_order.index(my_card) < self.card_order.index(other.cards[i]):
                    return False
        return False


class HandP2(Hand):
    def __init__(self, line: str):
        super().__init__(line)
        if "JJJJJ" == self.cards:
            self.type = "5"
        elif "J" in self.cards:
            self.type = min(
                (find_type(self.cards.replace("J", c)) for c in self.cards if c != "J"),
                key=lambda x: TYPES.index(x),
            )
        self.card_order = CARDS_P2


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    HANDS_P1 = [Hand(line) for line in DATA.split("\n")]
    print(sum(h.bid * i for i, h in enumerate(sorted(HANDS_P1), start=1)))

    HANDS_P2 = [HandP2(line) for line in DATA.split("\n")]
    print(sum(h.bid * i for i, h in enumerate(sorted(HANDS_P2), start=1)))
