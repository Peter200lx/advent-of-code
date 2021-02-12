from pathlib import Path
from typing import List, Union

import day12

INPUT_FILE = Path(__file__).with_suffix(".input")


def fast_simulate(a: int, b: int, c: int) -> bool:
    num_produced = 0
    last_produced = 1
    d = a + c * b
    while True:
        a = d
        while a != 0:
            b = a
            a = b // 2
            c = b % 2
            if c == last_produced:
                return False
            last_produced = c
            num_produced += 1
            if num_produced > 100:
                return True


def find_signal(program: List[List[Union[str, int]]]):
    c = program[1][1]
    b = program[2][1]
    for i in range(999999):
        if fast_simulate(i, b, c):
            return i


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    print(find_signal(day12.parse_data(DATA)))
