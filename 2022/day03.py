import string
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

VALUE = {c: i for i, c in enumerate(string.ascii_lowercase + string.ascii_uppercase, start=1)}


def sack_delta(sack: str) -> int:
    assert len(sack) % 2 == 0
    s1, s2 = sack[:len(sack)//2], sack[len(sack)//2:]
    return VALUE[next(iter(set(s1) & set(s2)))]


def part2(s1: str, s2: str, s3: str) -> int:
    return VALUE[next(iter(set(s1) & set(s2) & set(s3)))]

if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT_DATA = [line for line in DATA.split("\n")]

    print(sum(sack_delta(r) for r in INPUT_DATA))
    print(sum(part2(INPUT_DATA[i], INPUT_DATA[i+1], INPUT_DATA[i+2]) for i in range(0, len(INPUT_DATA), 3)))
