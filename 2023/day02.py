from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

PART_1 = {"red": 12, "green": 13, "blue": 14}


class Game:
    def __init__(self, line: str):
        game, rounds = line.split(": ")
        rounds = rounds.split("; ")
        self.id = int(game.split()[1])
        self.rounds = [
            {name: int(n) for part in r.split(", ") for n, name in [part.split()]}
            for r in rounds
        ]

    def possible(self, total):
        for round in self.rounds:
            for color, n in total.items():
                if round.get(color, 0) > n:
                    return False
        return True

    def min(self):
        totals = {"red": 0, "green": 0, "blue": 0}
        for round in self.rounds:
            for color in totals:
                totals[color] = max(totals[color], round.get(color, 0))
        return totals


def part_one(games):
    nums = 0
    for game in games:
        if game.possible(PART_1):
            nums += game.id
    return nums


def part_two(games):
    powers = 0
    for game in games:
        req = game.min()
        powers += req.get("red") * req.get("green") * req.get("blue")
    return powers


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT = [Game(line) for line in DATA.split("\n")]

    print(part_one(INPUT))
    print(part_two(INPUT))
