from collections import Counter
from pathlib import Path
import re

FILE_DIR = Path(__file__).parent

LINE = re.compile(r"([0-9]+)-([0-9]+) ([a-z]+): (.*)")


def parse_line(line):
    match = LINE.match(line)
    n1, n2, char, password = match.groups()
    return int(n1), int(n2), char, password


def validate_password(minnum, maxnum, char, password):
    return minnum <= Counter(password)[char] <= maxnum


def real_validate_password(first, second, char, password):
    a, b = (password[pos - 1] == char for pos in (first, second))
    return a != b


if __name__ == "__main__":
    DATA = (FILE_DIR / "day02.input").read_text().strip()
    INPUT = [parse_line(line) for line in DATA.split("\n")]
    print(sum(validate_password(*t) for t in INPUT))
    print(sum(real_validate_password(*t) for t in INPUT))
