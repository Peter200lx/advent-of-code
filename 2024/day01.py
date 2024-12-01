from collections import Counter
from pathlib import Path


INPUT_FILE = Path(__file__).with_suffix(".input")


def parse_lines(lines: list[str]) -> tuple[int, int]:
    first, second = [], []
    for line in lines:
        first_str, second_str = line[:6], line[6:]
        first.append(int(first_str))
        second.append(int(second_str))

    f_sort, s_sort = sorted(first), sorted(second)
    delta = list(map(lambda x: abs(x[0] - x[1]), (zip(f_sort, s_sort))))

    sim_score = 0
    count = Counter(second)
    for n in first:
        if n in count:
            sim_score += n * count[n]

    return sum(delta), sim_score


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT = DATA.split("\n")

    print(parse_lines(INPUT))
