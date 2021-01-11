import re

RE_NUMS = re.compile(r"-?\d+")

STARTING_CODE = 20151125
MULTIPLY_BY = 252533
MOD_BY = 33554393

DATA = """To continue, please consult the code grid in the manual.  Enter the code at row 3010, column 3019."""


def gen_fields(start_num: int, target_row: int = 1, target_column: int = 1) -> int:
    row = column = 1
    cur_num = start_num
    while True:
        if row == 1:
            column, row = 1, column + 1
        else:
            column += 1
            row -= 1
        cur_num = (cur_num * MULTIPLY_BY) % MOD_BY
        if row == target_row and column == target_column:
            return cur_num


if __name__ == "__main__":
    ROW, COLUMN = tuple(map(int, RE_NUMS.findall(DATA)))
    print(gen_fields(STARTING_CODE, ROW, COLUMN))
