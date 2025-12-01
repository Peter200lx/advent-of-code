from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

START = 50
MODULO = 100


def parse_lines(lines: list[str]) -> int:
    cur = START
    zero_count = 0
    total_zero_count = 0
    for line in lines:
        start = cur
        dirstr, amount = line[0], int(line[1:])
        direction = -1 if dirstr == "L" else 1
        cur += amount * direction
        tmp_cur = cur
        cur %= MODULO
        if tmp_cur != cur or cur == 0:
            if amount < MODULO:
                if start != 0:
                    total_zero_count += 1
            else:
                if start != 0:
                    total_zero_count += 1
                times = amount // MODULO
                # print(times)
                total_zero_count += times
        if cur == 0:
            zero_count += 1
    return zero_count  # , total_zero_count


def crude_p2(lines):
    cur = START
    total_zero_count = 0
    for line in lines:
        dirstr, amount = line[0], int(line[1:])
        direction = -1 if dirstr == "L" else 1
        for _ in range(amount):
            cur += direction
            cur %= MODULO
            if cur == 0:
                total_zero_count += 1
    return total_zero_count


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT = DATA.split("\n")

    print(parse_lines(INPUT))
    print(crude_p2(INPUT))
