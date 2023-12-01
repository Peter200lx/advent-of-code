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


def part_one(items):
    count = 0
    for item in items:
        first, second = None, None
        for c in item:
            if c.isdigit():
                if first is None:
                    first = c
                else:
                    second = c
        if second is None:
            second = first
        count += int(first + second)
    return count


def part_two(items):
    count = 0
    for item in items:
        first, second = None, None
        for i, c in enumerate(item):
            if c.isdigit():
                if first is None:
                    first = c
                else:
                    second = c
            else:
                for name, num in DIGITS.items():
                    if item[i:].startswith(name):
                        if first is None:
                            first = num
                        else:
                            second = num
        if second is None:
            second = first
        count += int(first + second)
    return count


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT = [line for line in DATA.split("\n")]

    print(part_one(INPUT))

    print(part_two(INPUT))
