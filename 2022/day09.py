from pathlib import Path
from typing import List, Tuple, NamedTuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Pos(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Pos") -> "Pos":
        return Pos(self.x + other.x, self.y + other.y)

    def follow(self, other: "Pos") -> "Pos":
        # This is assuming that 'other' is always within one movement from 'self'
        if abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1:
            return self
        elif abs(self.x - other.x) == 0:
            return Pos(self.x, self.y + (1 if other.y > self.y else -1))
        elif abs(self.y - other.y) == 0:
            return Pos(self.x + (1 if other.x > self.x else -1), self.y)
        else:  # Diagonal
            return Pos(
                x=self.x + (1 if other.x > self.x else -1),
                y=self.y + (1 if other.y > self.y else -1),
            )


START = Pos(0, 0)
DIR_MOVES = {
    "U": Pos(0, 1),
    "D": Pos(0, -1),
    "L": Pos(-1, 0),
    "R": Pos(1, 0),
}


def full_solve(inst: List[Tuple[str, int]], length=2) -> int:
    snake = [START] * length
    seen_tails = {snake[-1]}
    for direc, n in inst:
        for _i in range(n):
            snake[0] += DIR_MOVES[direc]
            for i in range(1, len(snake)):
                snake[i] = snake[i].follow(snake[i - 1])
            seen_tails.add(snake[-1])
    return len(seen_tails)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT_DATA = [(line[0], int(line[2:])) for line in DATA.split("\n")]

    print(full_solve(INPUT_DATA))
    print(full_solve(INPUT_DATA, 10))
