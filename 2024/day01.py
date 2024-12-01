from collections import Counter
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


def parse_lines(lines: list[str]) -> tuple[int, int]:
    first, second = [], []
    for line in lines:
        first.append(int(line[:6]))
        second.append(int(line[6:]))

    delta = list(map(lambda x: abs(x[0] - x[1]), (zip(sorted(first), sorted(second)))))

    count = Counter(second)

    return sum(delta), sum(n * count[n] for n in first if n in count)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT = DATA.split("\n")

    print(parse_lines(INPUT))
