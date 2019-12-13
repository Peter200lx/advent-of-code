from enum import Enum
from pathlib import Path
from typing import List, Tuple, Union

from processor import Processor


class TileID(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


def print_board(board: List[List[TileID]]) -> None:
    for row in board:
        print("".join(" #U=*"[i.value] if i.value else " " for i in row))


def read_output(
    output: List[int],
    board: List[List[TileID]],
    score: int = 0,
    ball_x: int = None,
    paddle_x: int = None,
) -> Tuple[int, int, int]:
    assert len(output) % 3 == 0
    for x, y, tid in (output[i : i + 3] for i in range(0, len(output), 3)):
        if x == -1:
            score = tid
        else:
            tile = TileID(tid)
            board[y][x] = tile
            if tile is TileID.BALL:
                ball_x = x
            elif tile is TileID.PADDLE:
                paddle_x = x
    return score, ball_x, paddle_x


def get_key() -> int:
    while True:
        key = getkey()
        if key == keys.LEFT:
            return -1
        elif key == keys.RIGHT:
            return 1
        elif key == keys.SPACE:
            return 0


def auto_key(ball_x: int, paddle_x: int) -> int:
    if paddle_x > ball_x:
        return -1
    elif paddle_x < ball_x:
        return 1
    else:
        return 0


def play_bot(
    program: List[int], part2: bool = False, debug: int = 0, manual: bool = False
) -> Union[int, List[List[TileID]]]:
    board = [[TileID.EMPTY for _ in range(37)] for _ in range(22)]
    override = [(0, 2)] if part2 else []
    running_bot = Processor(program, override, debug=debug).run_on_input_generator()
    output = next(running_bot)  # Get all output up to first input request
    score, ball_x, paddle_x = read_output(output, board)
    try:
        while True:
            if debug or manual:
                print_board(board)
                print(score)
            next_input = get_key() if manual else auto_key(ball_x, paddle_x)
            output = running_bot.send(next_input)
            score, ball_x, paddle_x = read_output(
                output, board, score, ball_x, paddle_x
            )

    except StopIteration:
        return score if part2 else board


if __name__ == "__main__":
    MANUAL = False
    if MANUAL:
        from getkey import getkey, keys
    DATA = Path("day13.input").read_text().strip()
    int_list = [int(i) for i in DATA.split(",")]

    print(sum(sum(t == TileID.BLOCK for t in r) for r in play_bot(int_list)))
    print(play_bot(int_list, part2=True, manual=MANUAL))
