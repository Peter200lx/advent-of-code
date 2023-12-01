from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

DIGITS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def parse_line(line: str, part2: bool = False) -> int:
    first, second = None, None
    for i, c in enumerate(line):
        if c.isdigit():
            if first is None:
                first = c
            else:
                second = c
        elif part2:
            for name, num in DIGITS.items():
                if line[i:].startswith(name):
                    if first is None:
                        first = num
                    else:
                        second = num
    if second is None:
        second = first
    return int(first + second)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT = DATA.split("\n")

    print(sum(parse_line(line) for line in INPUT))

    print(sum(parse_line(line, part2=True) for line in INPUT))
