from pathlib import Path
import re

FILE_DIR = Path(__file__).parent

LINE = re.compile(r"([0-9]+)-([0-9]+) ([a-z]+): (.*)")


def parse_line(line):
    match = LINE.match(line)
    n1, n2, char, password = match.groups()
    return int(n1), int(n2), char, password


def validate_password(minnum, maxnum, char, password):
    return minnum <= password.count(char) <= maxnum


def real_validate_password(first, second, char, password):
    return (password[first - 1] == char) != (password[second - 1] == char)


if __name__ == "__main__":
    DATA = (FILE_DIR / "day02.input").read_text().strip()
    INPUT = [parse_line(line) for line in DATA.split("\n")]
    print(sum(validate_password(*t) for t in INPUT))
    print(sum(real_validate_password(*t) for t in INPUT))
