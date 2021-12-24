from functools import lru_cache
from typing import Tuple
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


def processing(z, n, div1, add1, add2):
    # w = n
    # x = 0
    # x += z
    # x %= 26
    # z //= div1
    # x += add1
    x = (z % 26) + add1
    z //= div1
    # x = int(bool(x == w))
    # x = int(bool(x == 0))
    # y = 0
    # y+=25
    # y*=x
    # y+=1
    # z *= y
    # # z *= 26 if x != n else 1
    # y=0
    # y+=w
    # y+=add2
    # y*=x
    # z += y
    # # z += n + add2 if x != n else 0
    if x != n:
        z *= 26
        z += n + add2
    return z


@lru_cache(maxsize=None)
def solve(
    magic: Tuple[Tuple[int, int, int], ...], digits: range, z: int, depth: int = 0
) -> Tuple[int, ...]:
    ideal = (z % 26) + magic[depth][1]
    for digit in digits:
        if magic[depth][0] == 26 and ideal != digit:
            continue
        new_z = processing(z, digit, *magic[depth])
        if depth == 13:
            if new_z == 0:
                return digit,
        else:
            result = solve(magic, digits, new_z, depth + 1)
            if result:
                return (digit,) + result
    return tuple()


def p1p2(_instructions):
    magic = (
        (1, 11, 8),
        (1, 12, 8),
        (1, 10, 12),
        (26, -8, 10),
        (1, 15, 2),
        (1, 15, 8),
        (26, -11, 4),
        (1, 10, 9),
        (26, -3, 10),
        (1, 15, 3),
        (26, -3, 7),
        (26, -1, 7),
        (26, -10, 2),
        (26, -16, 2),
    )
    print("".join(str(d) for d in solve(magic, range(9, 0, -1), 0)))
    print("".join(str(d) for d in solve(magic, range(1, 10), 0)))


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    p1p2(DATA.split("\n"))
