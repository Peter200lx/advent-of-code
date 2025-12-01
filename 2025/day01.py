from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

START = 50
MODULO = 100


def parse_lines(lines: list[str]) -> tuple[int, int]:
    cur = START
    zero_count = 0
    p2_zero_count = 0
    for line in lines:
        start = cur
        dirstr, amount = line[0], int(line[1:])
        direction = -1 if dirstr == "L" else 1
        cur += amount * direction
        p2_zero_count += sum(x % MODULO == 0 for x in range(start, cur, direction))
        cur %= MODULO
        if cur == 0:
            zero_count += 1
    return zero_count, p2_zero_count


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT = DATA.split("\n")

    print("\n".join(str(x) for x in parse_lines(INPUT)))
