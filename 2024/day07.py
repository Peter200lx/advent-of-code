from itertools import product
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


def is_valid(test: int, vals: list[int], ops="*+") -> bool:
    for seq in product(ops, repeat=len(vals) - 1):
        result = vals[0]
        for i, c in enumerate(seq, start=1):
            if result > test:
                break
            if c == "*":
                result *= vals[i]
            elif c == "+":
                result += vals[i]
            else:
                result = int(f"{result}{vals[i]}")
        if result == test:
            return True
    return False


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    OPERATORS = [
        (int(left), [int(n) for n in right.split()])
        for line in DATA.split("\n")
        for left, right in [line.split(": ")]
    ]

    print(sum(l[0] for l in OPERATORS if is_valid(*l)))
    print(sum(l[0] for l in OPERATORS if is_valid(*l, ops="*+|")))
