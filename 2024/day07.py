from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


def is_valid(test: int, vals: list[int], so_far: int, ops="*+") -> bool:
    if so_far > test:
        return False
    if not vals:
        return so_far == test
    for op in ops:
        if op == "*" and is_valid(test, vals[1:], so_far * vals[0], ops):
            return True
        elif op == "+" and is_valid(test, vals[1:], so_far + vals[0], ops):
            return True
        elif op == "|" and is_valid(test, vals[1:], int(f"{so_far}{vals[0]}"), ops):
            return True
    return False


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    OPERATORS = [
        (int(left), [int(n) for n in right.split()])
        for line in DATA.split("\n")
        for left, right in [line.split(": ")]
    ]

    print(sum(t for t, o in OPERATORS if is_valid(t, o[1:], o[0])))
    print(sum(t for t, o in OPERATORS if is_valid(t, o[1:], o[0], ops="*+|")))
