from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


def parse_n(line: list[int]) -> bool:
    inc = None
    last_val = None
    for n in line:
        if last_val is None:
            last_val = n
        else:
            if not (1 <= abs(last_val - n) <= 3):
                return False
            if inc is None:
                inc = last_val < n
            else:
                if inc and last_val >= n:
                    return False
                if not inc and last_val <= n:
                    return False
            last_val = n
    return True


def p2(line: list[int]):
    if parse_n(line):
        return True
    for i in range(len(line)):
        if parse_n(line[:i] + line[i + 1 :]):
            return True
    return False


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT = [[int(n) for n in line.split()] for line in DATA.split("\n")]

    print(sum(parse_n(l) for l in INPUT))
    print(sum(p2(l) for l in INPUT))
