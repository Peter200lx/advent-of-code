from enum import Enum
from pathlib import Path
from typing import NamedTuple, Dict, List

from processor import Processor


class TileID(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


class Point(NamedTuple):
    y: int
    x: int


def run_bot(program: List[int]) -> Dict[Point, TileID]:
    running_bot = Processor(program).run_on_output_generator(output_batch=3)
    next(running_bot)  # Prime the pump to the first yield for .send( below
    board = {}
    try:
        while True:
            x, y, tid = running_bot.send(None)
            board[Point(y, x)] = TileID(tid)
    except StopIteration:
        return board


def print_board(board: List[List[TileID]]) -> None:
    for row in board:
        print("".join(" #U=*"[i.value] if i.value else " " for i in row))


def get_key():
    while True:
        key = getkey()
        if key == keys.LEFT:
            return -1
        elif key == keys.RIGHT:
            return 1
        elif key == keys.SPACE:
            return 0


def read_output(output, board, score=0, ball_x=None, paddle_x=None):
    assert len(output) % 3 == 0
    for x, y, tid in (output[i : i + 3] for i in range(0, len(output), 3)):
        if x == -1:
            score = tid
        else:
            board[y][x] = TileID(tid)
            if tid == TileID.BALL.value:
                ball_x = x
            elif tid == TileID.PADDLE.value:
                paddle_x = x
    return score, ball_x, paddle_x


def play_bot(program, debug=False, manual=False):
    running_bot = Processor(program, ((0, 2),)).run_on_input_generator()
    output = next(running_bot)  # Get all output up to first input request
    board = [[TileID.EMPTY for _ in range(37)] for _ in range(22)]
    score, ball_x, paddle_x = read_output(output, board)
    next_input = 0
    try:
        while True:
            output = running_bot.send(next_input)
            score, ball_x, paddle_x = read_output(
                output, board, score, ball_x, paddle_x
            )
            if debug or manual:
                print_board(board)
                print(score)
            if manual:
                next_input = get_key()
            else:
                if paddle_x > ball_x:
                    next_input = -1
                elif paddle_x < ball_x:
                    next_input = 1
                else:
                    next_input = 0

    except StopIteration:
        return score


if __name__ == "__main__":
    MANUAL = False
    if MANUAL:
        from getkey import getkey, keys
    DATA = Path("day13.input").read_text().strip()
    int_list = [int(i) for i in DATA.split(",")]

    print(sum(v == TileID.BLOCK for v in run_bot(int_list).values()))
    print(play_bot(int_list, manual=MANUAL))
