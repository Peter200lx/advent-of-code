from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, NamedTuple

FILE_DIR = Path(__file__).parent

SIZE = 5


class Coord(NamedTuple):
    x: int
    y: int


WINNING_COMBOS = [
    *({Coord(x, y) for y in range(SIZE)} for x in range(SIZE)),
    *({Coord(x, y) for x in range(SIZE)} for y in range(SIZE)),
]


@dataclass()
class Square:
    num: int
    coord: Coord
    marked: bool


def parse_input(lines: str) -> Tuple[List[int], List[Dict[Coord, Square]]]:
    num_line, *board_lines = lines.split("\n\n")
    nums = [int(i) for i in num_line.split(",")]

    boards = [
        {
            Coord(x, y): Square(int(num), Coord(x, y), False)
            for y, line in enumerate(board.split("\n"))
            for x, num in enumerate(line.split())
        }
        for board in board_lines
    ]
    return nums, boards


def check_lines(board: Dict[Coord, Square]) -> bool:
    return any(all(board[coord].marked for coord in combo) for combo in WINNING_COMBOS)


def solve(
    draws: List[int], boards: List[Dict[Coord, Square]], part1: bool = True
) -> Tuple[int, int]:
    done = set()
    for num in draws:
        for board in boards:
            if id(board) in done:
                continue
            square = [sq for sq in board.values() if sq.num == num]
            if not square:
                continue
            square[0].marked = True
            if check_lines(board):
                if part1:
                    return num, sum(sq.num for sq in board.values() if not sq.marked)
                done.add(id(board))
                if len(done) == len(boards):
                    return num, sum(sq.num for sq in board.values() if not sq.marked)


if __name__ == "__main__":
    DATA = (FILE_DIR / "day04.input").read_text().strip()

    DRAWS, BOARDS = parse_input(DATA)

    P1NUM, P1SUM = solve(DRAWS, BOARDS)
    print(P1NUM * P1SUM)
    P2NUM, P2SUM = solve(DRAWS, BOARDS, part1=False)
    print(P2NUM * P2SUM)
