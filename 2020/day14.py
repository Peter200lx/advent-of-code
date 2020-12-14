import re
from functools import reduce
from itertools import combinations
from operator import ior
from pathlib import Path

FILE_DIR = Path(__file__).parent

MASK_LEN = 36
RE_NUMS = re.compile(r"-?\d+")


class Computer:
    def __init__(self):
        self.mask_clear_bits = 0
        self.mask_set_bits = 0
        self.mask_float = set()
        self.memory = {}

    def read_line(self, line: str):
        if line.startswith("mask"):
            _whocares, mask_str = line.split(" = ")
            self.mask_clear_bits = int(mask_str.replace("X", "1"), 2)
            self.mask_set_bits = int(mask_str.replace("X", "0"), 2)
        else:
            addr, value = list(map(int, RE_NUMS.findall(line)))
            value &= self.mask_clear_bits
            value |= self.mask_set_bits
            self.memory[addr] = value

    def generate_floating_masks(self, number):
        number |= self.mask_set_bits
        clear_bits = reduce(ior, ((1 << i) for i in self.mask_float), 0)
        number &= ~clear_bits
        for comb_size in range(len(self.mask_float) + 1):
            for combination in combinations(self.mask_float, comb_size):
                set_bits = reduce(ior, (1 << i for i in combination), 0)
                yield number | set_bits

    def read_line_mass_write(self, line: str):
        if line.startswith("mask"):
            _whocares, mask_str = line.split(" = ")
            self.mask_set_bits = int(mask_str.replace("X", "0"), 2)
            self.mask_float = {i for i, s in enumerate(reversed(mask_str)) if s == "X"}
        else:
            addr, value = list(map(int, RE_NUMS.findall(line)))
            for to_write_addr in self.generate_floating_masks(addr):
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
