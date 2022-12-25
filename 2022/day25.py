from pathlib import Path
from typing import List

INPUT_FILE = Path(__file__).with_suffix(".input")


READ = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}


def parse_5(in_str: str) -> int:
    result = 0
    for i, c in enumerate(in_str[::-1]):
        result += READ[c] * 5**i
    return result


def to_5(num: int) -> List[str]:
    processed = num
    result = []
    while processed:
        res = processed % 5
        if res in range(0, 3):
            result.append(str(res))
            processed //= 5
        elif res == 3:
            result.append("=")
            processed = (processed + 2) // 5
        elif res == 4:
            result.append("-")
            processed = (processed + 1) // 5
    result.reverse()
    return result


def part_1(ints: List[int]) -> str:
    in_sum = sum(ints)
    return "".join(to_5(in_sum))


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().rstrip()
    INTS = [parse_5(line) for line in DATA.split("\n")]

    print(part_1(INTS))
