from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INSTRUCTIONS = [[char for char in line] for line in DATA.split("\n")]

    GRID = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]

    MIN_LOC = 0
    MAX_LOC = 2

    MOVE_MAP = {
        "U": (0, -1),
        "D": (0, 1),
        "L": (1, -1),
        "R": (1, 1),
    }

    def move(position, direction):
        movement = MOVE_MAP[direction]
        new_val = position[movement[0]] + movement[1]
        if new_val > MAX_LOC or new_val < MIN_LOC:
            return position
        position[movement[0]] = new_val
        return position

    def val_at_loc(grid, position):
        return grid[position[0]][position[1]]

    cur_pos = [1, 1]  # y, x
    code = ""

    for inst in INSTRUCTIONS:
        for direction in inst:
            # print(f"{val_at_loc(GRID, cur_pos)} moving {direction}")
            cur_pos = move(cur_pos, direction)
        # print(f"--- {code or '<>'} adding {val_at_loc(GRID, cur_pos)}")
        code += str(val_at_loc(GRID, cur_pos))

    print(code)

    # fmt: off
    GRID = [
        [None, None,   1 , None, None],
        [None,   2 ,   3 ,   4 , None],
        [  5 ,   6 ,   7 ,   8 ,   9 ],
        [None,  "A",  "B",  "C", None],
        [None,  None, "D", None, None],
    ]
    # fmt: on

    MIN_LOC = 0
    MAX_LOC = 4

    cur_pos = [3, 0]  # y, x
    code = ""

    def move(position, direction):
        movement = MOVE_MAP[direction]
        old_pos = list(position)
        new_val = position[movement[0]] + movement[1]
        if new_val > MAX_LOC or new_val < MIN_LOC:
            return position
        position[movement[0]] = new_val
        if val_at_loc(GRID, position) is None:
            return old_pos
        return position

    for inst in INSTRUCTIONS:
        for direction in inst:
            # print(f"{val_at_loc(GRID, cur_pos)} moving {direction}")
            cur_pos = move(cur_pos, direction)
        # print(f"--- {code or '<>'} adding {val_at_loc(GRID, cur_pos)}")
        code += str(val_at_loc(GRID, cur_pos))

    print(code)
