from pathlib import Path
from typing import List, Tuple

INPUT_FILE = Path(__file__).with_suffix(".input")


def calc_both(moves: List[Tuple[str, int]]) -> Tuple[int, int]:
    forward = depth1aim = depth2 = 0
    for direction, n in moves:
        if direction == "up":
            depth1aim -= n
        elif direction == "down":
            depth1aim += n
        else:
            forward += n
            depth2 += depth1aim * n
    return depth1aim * forward, depth2 * forward


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT = [(d, int(n)) for line in DATA.split("\n") for d, n in [line.split()]]

    print(calc_both(INPUT))
