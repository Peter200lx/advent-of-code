from typing import List, Tuple
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

import numpy as np

np.set_printoptions(linewidth=100)

EXAMPLE_DATA = """     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ """
LETTERS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
POSS_NEXT = LETTERS | {"-", "|"}
DIR_SLICE = {
    "N": lambda y, x: (slice(y, None, -1), x),
    "S": lambda y, x: (slice(y, None), x),
    "E": lambda y, x: (y, slice(x, None)),
    "W": lambda y, x: (y, slice(x, None, -1)),
}
g_counter = 0


class MazeEnd(Exception):
    pass


def calc_next_vect(board: np.ndarray, old_vect: Tuple[str, int, int], movement: int) -> Tuple[str, int, int]:
    dir_str, y, x = old_vect
    delta = movement * (1 if dir_str in ("S", "E") else -1)
    if dir_str in ("N", "S"):
        y += delta
        if (x - 1) >= 0 and board[y, x - 1] in POSS_NEXT:
            new_dir = "W"
        elif (x + 1) < board.shape[1] and board[y, x + 1] in POSS_NEXT:
            new_dir = "E"
        else:
            raise IndexError(f"Didn't find next move from {x} in {board[y, :]}")
    elif dir_str in ("E", "W"):
        x += delta
        if (y - 1) >= 0 and board[y - 1, x] in POSS_NEXT:
            new_dir = "N"
        elif (y + 1) < board.shape[0] and board[y + 1, x] in POSS_NEXT:
            new_dir = "S"
        else:
            raise IndexError(f"Didn't find next move from {y} in {board[:, x]}")
    else:
        raise ValueError(f"Unknown direction {dir_str}")
    return new_dir, y, x


def follow_line(result_str: List[str], line: np.ndarray) -> int:
    global g_counter
    for i in range(1, len(line)):
        g_counter += 1
        if line[i] in LETTERS:
            result_str.append(line[i])
        elif line[i] == "+":
            return i
        elif line[i] == " ":
            raise MazeEnd(f"Maze ended with string {''.join(result_str)} after {g_counter} steps")


def follow_maze(board_str: str):
    maze_string = []
    board = np.array([list(l) for l in board_str.split("\n")])
    # print(board)
    starting_column = np.where(board[0, :] == "|")[0][0]
    vector = ("S", 0, starting_column)
    while True:
        # print(vector)
        line = board[DIR_SLICE[vector[0]](*vector[1:])]
        # print(line)
        end_loc_diff = follow_line(maze_string, line)
        vector = calc_next_vect(board, vector, end_loc_diff)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip("\n")
    try:
        follow_maze(DATA)
    except MazeEnd as result:
        print(result)
