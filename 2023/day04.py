from pathlib import Path
from typing import List

INPUT_FILE = Path(__file__).with_suffix(".input")


class Card:
    def __init__(self, line: str):
        card, rest = line.split(": ")
        self.id = int(card.split()[1])
        winning, have = rest.split(" | ")
        self.winning = {int(s) for s in winning.split() if s}
        self.have = {int(s) for s in have.split() if s}

    def __repr__(self):
        return f"Card({self.id}, {self.winning=}, {self.have=})"

    def worth(self) -> int:
        values = self.winning & self.have
        result = 0
        if values:
            result = 1
            for i in range(len(values) - 1):
                result *= 2
        return result


def part_two(card_list: List[Card]):
    cards = {c.id: c for c in card_list}
    cards_we_have = {c.id: 1 for c in card_list}
    for i in range(1, len(card_list) + 1):
        extras = len(cards[i].winning & cards[i].have)
        for j in range(1, extras + 1):
            cards_we_have[i + j] += cards_we_have[i]
    return sum(v for v in cards_we_have.values())


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    CARDS = [Card(line) for line in DATA.split("\n")]

    print(sum(c.worth() for c in CARDS))

    print(part_two(CARDS))
