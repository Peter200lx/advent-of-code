from pathlib import Path
from typing import List

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


def solve(lines: List[str], part2: bool = False) -> int:
    count = 0
    for line in lines:
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
        count += int(first + second)
    return count


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT = [line for line in DATA.split("\n")]

    print(solve(INPUT))

    print(solve(INPUT, part2=True))
