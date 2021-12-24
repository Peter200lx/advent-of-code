from functools import lru_cache
from typing import Tuple
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


def parse_section(lines: str) -> Tuple[int, int, int]:
    lines = lines.split("\n")
    *op, div1 = lines[3].split()
    assert op == ["div", "z"]
    *op, add1 = lines[4].split()
    assert op == ["add", "x"]
    *op, add2 = lines[14].split()
    assert op == ["add", "y"]
    return int(div1), int(add1), int(add2)


def processing(z, n, div1, add1, add2):
    # w = n
    # x = 0
    # x += z
    # x %= 26
    # z //= div1  # DO NOT HAVE THIS BEFORE x=(z%26)+add1
    # x += add1
    x = (z % 26) + add1
    z //= div1
    # x = int(bool(x == w))
    # x = int(bool(x == 0))
    # y = 0
    # y += 25
    # y *= x
    # y += 1
    # z *= y
    # # z *= 26 if x != n else 1
    # y = 0
    # y += w
    # y += add2  # IF YOU NAME THIS add2, DO NOT use *=  /)_-)
    # y *= x
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
                return (digit,)
        else:
            result = solve(magic, digits, new_z, depth + 1)
            if result:
                return (digit,) + result
    return tuple()


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    MAGIC_NUMS = tuple(
        parse_section(lines.strip()) for lines in DATA.split("inp w") if lines.strip()
    )
    print("".join(str(d) for d in solve(MAGIC_NUMS, range(9, 0, -1), 0)))
    print("".join(str(d) for d in solve(MAGIC_NUMS, range(1, 10), 0)))
