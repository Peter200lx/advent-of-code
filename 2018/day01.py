from pathlib import Path

FILE_DIR = Path(__file__).parent

START = 0


def calc(start, list_o_cal):
    return start + sum(list_o_cal)


def calc_v2(start, list_o_cal):
    cur = start
    found_set = {start}
    while True:
        for i in list_o_cal:
            cur += i
            if cur in found_set:
                return cur
            found_set.add(cur)


if __name__ == "__main__":
    DATA = (FILE_DIR / "day01.input").read_text().strip()

    int_list = [int(i) for i in DATA.split("\n")]
    print(calc(START, int_list))
    print(calc_v2(START, int_list))
