from typing import List
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

EXAMPLE_DATA = """0
3
0
1
-3"""


def part_1(instructions: List[int]) -> int:
    current_location = 0
    count = 0
    while 0 <= current_location < len(instructions):
        movement = instructions[current_location]
        instructions[current_location] += 1
        current_location += movement
        count += 1

    return count


def part_2(instructions: List[int]) -> int:
    current_location = 0
    count = 0
    while 0 <= current_location < len(instructions):
        movement = instructions[current_location]
        if movement >= 3:
            instructions[current_location] -= 1
        else:
            instructions[current_location] += 1
        current_location += movement
        count += 1

    return count


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INSTRUCTIONS = [int(i) for i in DATA.split("\n")]
    print(part_1(INSTRUCTIONS.copy()))
    print(part_2(INSTRUCTIONS.copy()))
