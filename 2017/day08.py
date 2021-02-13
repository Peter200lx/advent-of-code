from typing import Dict, List, Tuple
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

EXAMPLE_DATA = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""


def parse_instructions(instructions: List[List[str]]) -> Tuple[Dict[str, int], int]:
    registers = {}
    max_value = 0

    for inst in instructions:
        if inst[0] not in registers:
            registers[inst[0]] = 0
        if inst[4] not in registers:
            registers[inst[4]] = 0
        assert inst[5] in ("<", ">", "==", "<=", ">=", "!=")
        if eval(f"{registers[inst[4]]} {inst[5]} {int(inst[6])}"):
            assert inst[1] in ("inc", "dec")
            registers[inst[0]] += int(inst[2]) * (1 if "inc" == inst[1] else -1)
            max_value = max(max_value, registers[inst[0]])

    return registers, max_value


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INSTRUCTIONS = [[chunk for chunk in line.split()] for line in DATA.split("\n")]
    REGISTERS, MAX_VAL = parse_instructions(INSTRUCTIONS)
    print(max(REGISTERS.values()))
    print(REGISTERS)
    print(MAX_VAL)
