"""
I'm aware that there are better hex coordinate systems, but this was one that
I came up with on my own, and I wanted to prove that it could work. Work it
does, but it isn't super efficient.

(4,-1)   (4,0)   (4,1)   (4,2)
    (3,-1) | (3,0)   (3,1)   (3,2)
(2,-1)   (2,0)   (2,1)   (2,2)
    (1,-1) | (1,0)   (1,1)   (1,2)
(0,-1)---(0,0)---(0,1)---(0,2)------
   (-1,-1) | (-1,0)  (-1,1)  (-1,2)
(-2,-1) (-2,0)  (-2,1)  (-2,2)

     ^      |            /\
 sw  |  nw  |   (1,-1) /    \ (1,0)
   \ W /    |        /        \
    \|/     |       |          |
<-S-- --N-> | (0,-1)|   (0,0)  |  (0,1)
    /|\     |       |          |
   / E \    |        \        /
 se  |  ne  |  (-1,-1) \    / (-1,0)
     v      |            \/
"""

from typing import List, Tuple
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

TEST_DATA = {
    "ne,ne,ne": 3,
    "ne,ne,sw,sw": 0,
    "ne,ne,s,s": 2,
    "se,sw,se,sw,sw": 3,
}

# Originally I had a wrong number of directions for a hex grid,
#  and my "next closest" calculation broke with a distance of 2.
# I was able to solve this by rotating my compass directions 90deg.
# EVEN_MOVE_DICT = {'n': (2, 0),
#                   's': (-2, 0),
#                   # 'e': (0, 1),
#                   # 'w': (0, -1),
#                   'ne': (1, 0),
#                   'nw': (1, -1),
#                   'se': (-1, 0),
#                   'sw': (-1, -1)}
EVEN_MOVE_DICT = {
    "n": (0, 1),
    "s": (0, -1),
    "ne": (-1, 0),
    "nw": (1, 0),
    "se": (-1, -1),
    "sw": (1, -1),
}
EVEN_REV_MOVE = {k: v for (v, k) in EVEN_MOVE_DICT.items()}

ODD_MOVE_DICT = {
    "n": (0, 1),
    "s": (0, -1),
    "ne": (-1, 1),
    "nw": (1, 1),
    "se": (-1, 0),
    "sw": (1, 0),
}
ODD_REV_MOVE = {k: v for (v, k) in ODD_MOVE_DICT.items()}

g_max_steps = 0


def move(cur_loc: Tuple[int, int], step: str) -> Tuple[int, int]:
    movement = EVEN_MOVE_DICT[step] if (cur_loc[0] % 2) == 0 else ODD_MOVE_DICT[step]
    return cur_loc[0] + movement[0], cur_loc[1] + movement[1]


def move_steps(steps: List[str]) -> Tuple[int, int]:
    location = (0, 0)
    global g_max_steps
    for step in steps:
        location = move(location, step)
        g_max_steps = max(g_max_steps, shortest_path(location))
    return location


def find_closest(curr_loc: Tuple[int, int], dest: Tuple[int, int]) -> str:
    direction = dest[0] - curr_loc[0], dest[1] - curr_loc[1]
    use_dict = EVEN_REV_MOVE if (curr_loc[0] % 2) == 0 else ODD_REV_MOVE
    best_move = min(use_dict.keys(), key=lambda c: (c[0] - direction[0]) ** 2 + (c[1] - direction[1]) ** 2)
    return use_dict[best_move]


def shortest_path(destination: Tuple[int, int]) -> int:
    move_list = []
    cur_loc = (0, 0)
    while cur_loc != destination:
        step = find_closest(cur_loc, destination)
        move_list.append(step)
        cur_loc = move(cur_loc, step)
    # print(f"Moves: {move_list} give # of steps: {len(move_list)}")
    return len(move_list)


def run_test():
    for seq in TEST_DATA:
        location = (0, 0)
        for step in [s for s in seq.split(",")]:
            location = move(location, step)
        # print(location)
        min_steps = shortest_path(location)
        assert TEST_DATA[seq] == min_steps
        # print("\n--------------------------\n")


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    run_test()

    target_location = move_steps([s for s in DATA.split(",")])
    print(target_location)
    print(shortest_path(target_location))
    print(g_max_steps)
