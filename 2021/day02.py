from pathlib import Path

FILE_DIR = Path(__file__).parent


def parse_line(line):
    direction, num = line.split()
    return direction, int(num)


def part1(moves):
    forward = sum(n for d, n in moves if d == "forward")
    depth = sum(n if d == "down" else -n for d, n in INPUT if d != "forward")
    return forward * depth


def part2(moves):
    aim = forward = depth = 0
    for direction, n in moves:
        if direction == "up":
            aim -= n
        elif direction == "down":
            aim += n
        else:
            forward += n
            depth += aim * n
    return depth * forward


if __name__ == "__main__":
    DATA = (FILE_DIR / "day02.input").read_text().strip()
    INPUT = [parse_line(line) for line in DATA.split("\n")]

    print(part1(INPUT))
    print(part2(INPUT))
