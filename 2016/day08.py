from pathlib import Path

import numpy as np

INPUT_FILE = Path(__file__).with_suffix(".input")

np.set_printoptions(linewidth=120)

example_data = """rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1"""
"""
###....
###....
.......

#.#....
###....
.#.....

....#.#
###....
.#.....

.#..#.#
#.#....
.#.....
"""


def draw_rect(disp, square) -> None:
    x, y = square.split("x")
    x = int(x)
    y = int(y)
    disp[0:y, 0:x] = 1


def rotate_rect(disp, rc: str, selector: str, _, num: str) -> None:
    xy, which = selector.split("=")
    which = int(which)
    num = int(num)
    if rc == "column":
        assert xy == "x"
        disp[:, which] = np.roll(disp[:, which], num)
    elif rc == "row":
        assert xy == "y"
        disp[which, :] = np.roll(disp[which, :], num)
    else:
        raise ValueError("Second message must be 'row' or 'column'")


def run_example(data):
    disp = np.zeros((3, 7), dtype=np.uint8)
    print(disp)
    instructions = [[word for word in line.split()] for line in data.split("\n")]
    for inst in instructions:
        cmd_map[inst[0]](disp, *inst[1:])
        print(disp)


def disp_print(disp):
    for row in disp:
        line = ""
        for value in row:
            line += "█" if value else " "
        print(line)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INSTRUCTIONS = [[word for word in line.split()] for line in DATA.split("\n")]

    # run_example(example_data)

    display = np.zeros((6, 50), dtype=np.uint8)
    cmd_map = {"rect": draw_rect, "rotate": rotate_rect}

    for inst in INSTRUCTIONS:
        cmd_map[inst[0]](display, *inst[1:])

    print(display.sum())
    disp_print(display)
    # print(display)
    # ZJHRKCPLYJ
