from pathlib import Path
from typing import List, Tuple

FILE_DIR = Path(__file__).parent


def calc_both(moves: List[Tuple[str, int]]) -> Tuple[int, int]:
    aim = forward = depth1 = depth2 = 0
    for direction, n in moves:
        if direction == "up":
            aim -= n
            depth1 -= n
        elif direction == "down":
            aim += n
            depth1 += n
        else:
            forward += n
            depth2 += aim * n
    return depth1 * forward, depth2 * forward


if __name__ == "__main__":
    DATA = (FILE_DIR / "day02.input").read_text().strip()
    INPUT = [(d, int(n)) for line in DATA.split("\n") for d, n in [line.split()]]

    print(calc_both(INPUT))
