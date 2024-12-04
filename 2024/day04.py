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
# fmt: on
p2_o = [
    (
        (Coord(-1, -1), Coord(1, -1), Coord(-1, 1), Coord(1, 1)),
        ((0, 0, 2, 2), (0, 2, 0, 2)),
    ),
    (
        (Coord(-1, 1), Coord(1, 1), Coord(-1, -1), Coord(1, -1)),
        ((0, 0, 2, 2), (0, 2, 0, 2)),
    ),
    (
        (Coord(1, -1), Coord(-1, -1), Coord(1, 1), Coord(-1, 1)),
        ((0, 0, 2, 2), (0, 2, 0, 2)),
    ),
    (
        (Coord(1, 1), Coord(-1, 1), Coord(1, -1), Coord(-1, -1)),
        ((0, 0, 2, 2), (0, 2, 0, 2)),
    ),
]


def parse_table(in_str: str) -> dict[Coord, str]:
    lines = [line for line in in_str.split("\n")]
    assert all(len(lines[0]) == len(line) for line in lines)
    board = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            board[Coord(x, y)] = c
    return board


def p1(board: dict[Coord, str]) -> int:
    count = 0
    for coord in board:
        if board[coord] != P1_KEY[0]:
            continue
        for direc in p1_d:
            new_loc = coord
            found = True
            for i, c in enumerate(P1_KEY[1:], start=1):
                new_loc += direc
                new_c = board.get(new_loc)
                if c != new_c:
                    found = False
                    break
            if found:
                count += 1
    return count


def p2(board: dict[Coord, str]) -> int:
    count = 0
    for coord in sorted(board):
        if board[coord] != P2_KEY[1]:
            continue
        for orientation in p2_o:
            direc, seqs = orientation
            for seq in seqs:
                found = True
                for i in range(4):
                    if board.get(coord + direc[i]) != P2_KEY[seq[i]]:
                        found = False
                        break
                if found:
                    break
            if found:
                count += 1
                break
    return count


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    BOARD = parse_table(DATA)

    print(p1(BOARD))
    print(p2(BOARD))
