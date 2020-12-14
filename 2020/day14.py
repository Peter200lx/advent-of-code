import re
from collections import defaultdict
from itertools import combinations
from pathlib import Path

FILE_DIR = Path(__file__).parent

MASK_LEN = 36
RE_NUMS = re.compile(r"-?\d+")


class Computer:
    final_mask = int("1" * MASK_LEN, 2)

    def __init__(self):
        self.mask_and = 0
        self.mask_or = 0
        self.mask_float = set()
        self.memory = defaultdict(int)

    def read_line(self, line: str):
        if line.startswith("mask"):
            _whocares, mask_str = line.split(" = ")
            self.mask_and = int("".join("0" if s == "0" else "1" for s in mask_str), 2)
            self.mask_or = int("".join("1" if s == "1" else "0" for s in mask_str), 2)
        else:
            addr, value = list(map(int, RE_NUMS.findall(line)))
            value &= self.mask_and
            value |= self.mask_or
            self.memory[addr] = value

    def generate_floating_masks(self, floating_bits, number):
        number |= self.mask_or
        clear_bits = 0
        for n in ((1 << i) for i in floating_bits):
            clear_bits |= n
        number &= ~clear_bits
        for combination in (c for size in range(len(self.mask_float) + 1) for c in combinations(self.mask_float, size)):
            set_bits = 0
            for n in (1 << i for i in combination):
                set_bits |= n
            yield number | set_bits

    def read_line_mass_write(self, line: str):
        if line.startswith("mask"):
            _whocares, mask_str = line.split(" = ")
            self.mask_and = int("".join("0" if s == "0" else "1" for s in mask_str), 2)
            self.mask_or = int("".join("1" if s == "1" else "0" for s in mask_str), 2)
            self.mask_float = {i for i, s in enumerate(reversed(mask_str)) if s == "X"}
        else:
            addr, value = list(map(int, RE_NUMS.findall(line)))
            for to_write_addr in self.generate_floating_masks(self.mask_float, addr):
                self.memory[to_write_addr] = value

    def sum_mem(self):
        return sum(self.memory.values())


if __name__ == "__main__":
    DATA = (FILE_DIR / "day14.input").read_text().strip()
    comp_p1 = Computer()
    for instruction in DATA.split("\n"):
        comp_p1.read_line(instruction)
    print(comp_p1.sum_mem())
    comp_p2 = Computer()
    for instruction in DATA.split("\n"):
        comp_p2.read_line_mass_write(instruction)
    print(comp_p2.sum_mem())
