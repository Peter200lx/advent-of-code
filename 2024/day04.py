from pathlib import Path
from typing import NamedTuple

INPUT_FILE = Path(__file__).with_suffix(".input")

P1_KEY = "XMAS"
P2_KEY = "MAS"


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)


# fmt: off
p1_d = [Coord(-1, -1), Coord(0, -1), Coord(1, -1),
        Coord(-1, 0),                Coord(1, 0),
        Coord(-1, 1),  Coord(0, 1),  Coord(1, 1)]
p2_d = [Coord(-1, -1), Coord(1, -1),
        Coord(-1, 1),  Coord(1, 1)]
# fmt: on


def p1(board: dict[Coord, str]) -> int:
    count = 0
    for coord in board:
        if board[coord] != P1_KEY[0]:
            continue
        for direc in p1_d:
            new_loc = coord
            found = True
            for c in P1_KEY[1:]:
                new_loc += direc
                if c != board.get(new_loc):
                    found = False
                    break
            if found:
                count += 1
    return count


def p2(board: dict[Coord, str]) -> int:
    count = 0
    for coord in board:
        if board[coord] != P2_KEY[1]:
            continue
        new_locs = [coord + d for d in p2_d]
        for seq in ((0, 0, 2, 2), (0, 2, 0, 2), (2, 2, 0, 0), (2, 0, 2, 0)):
            found = True
            for i in range(4):
                if board.get(new_locs[i]) != P2_KEY[seq[i]]:
                    found = False
                    break
            if found:
                break
        if found:
            count += 1
    return count


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    BOARD = {
        Coord(x, y): c
        for y, line in enumerate(DATA.split("\n"))
        for x, c in enumerate(line)
    }

    print(p1(BOARD))
    print(p2(BOARD))
