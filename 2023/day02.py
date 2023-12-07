from math import prod
from pathlib import Path
from typing import Dict

INPUT_FILE = Path(__file__).with_suffix(".input")

PART_1 = {"red": 12, "green": 13, "blue": 14}


class Game:
    def __init__(self, line: str):
        game, rounds = line.split(": ")
        self.id = int(game.split()[1])
        self.rounds = [
            {name: int(n) for part in r.split(", ") for n, name in [part.split()]}
            for r in rounds.split("; ")
        ]

    def possible(self, req: Dict[str, int]) -> bool:
        return not any(turn.get(color, 0) > n for color, n in req.items() for turn in self.rounds)

    def req(self) -> Dict[str, int]:
        totals = {"red": 0, "green": 0, "blue": 0}
        for turn in self.rounds:
            for color in totals:
                totals[color] = max(totals[color], turn.get(color, 0))
        return totals


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT = [Game(line) for line in DATA.split("\n")]

    print(sum(game.id for game in INPUT if game.possible(PART_1)))
    print(sum(prod(game.req().values()) for game in INPUT))
