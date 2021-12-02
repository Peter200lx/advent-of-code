from pathlib import Path

FILE_DIR = Path(__file__).parent


def parse_line(line):
    direction, num = line.split()
    return direction, int(num)


def calc_both(moves):
    aim = forward = depth1 = depth2 = 0
    for direction, n in moves:
        if direction == "up":
            aim -= n
            depth1 -= n
        elif direction == "down":
            aim += n
            depth1 += n
        else:
            forward += n
            depth2 += aim * n
    return depth1 * forward, depth2 * forward


if __name__ == "__main__":
    DATA = (FILE_DIR / "day02.input").read_text().strip()
    INPUT = [parse_line(line) for line in DATA.split("\n")]

    print(calc_both(INPUT))
