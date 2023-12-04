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

    def num_match(self) -> int:
        return len(self.winning & self.have)

    def worth(self) -> int:
        return 2 ** (self.num_match() - 1) if self.num_match() else 0


def part_two(card_list: List[Card]) -> int:
    cards_we_have = {c.id: 1 for c in card_list}
    for i, card in enumerate(card_list, start=1):
        for j in range(1, card.num_match() + 1):
            cards_we_have[i + j] += cards_we_have[i]
    return sum(v for v in cards_we_have.values())


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    CARDS = [Card(line) for line in DATA.split("\n")]

    print(sum(c.worth() for c in CARDS))

    print(part_two(CARDS))
