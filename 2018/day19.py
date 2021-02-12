from collections import namedtuple
from functools import reduce
from typing import List

from day16 import Processor

DATA = """#ip 4
addi 4 16 4
seti 1 5 1
seti 1 7 3
mulr 1 3 5
eqrr 5 2 5
addr 5 4 4
addi 4 1 4
addr 1 0 0
addi 3 1 3
gtrr 3 2 5
addr 4 5 4
seti 2 4 4
addi 1 1 1
gtrr 1 2 5
addr 5 4 4
seti 1 5 4
mulr 4 4 4
addi 2 2 2
mulr 2 2 2
mulr 4 2 2
muli 2 11 2
addi 5 2 5
mulr 5 4 5
addi 5 18 5
addr 2 5 2
addr 4 0 4
seti 0 6 4
setr 4 3 5
mulr 5 4 5
addr 4 5 5
mulr 4 5 5
muli 5 14 5
mulr 5 4 5
addr 2 5 2
seti 0 2 0
seti 0 6 4"""


Cmd = namedtuple("CMD", ["op", "a", "b", "c"])


class Day19Processor(Processor):
    def __init__(self, jump_reg: int, program: List[Cmd]):
        self.pc_loc = jump_reg
        self.registers = [0] * 6
        self.program = program

    @property
    def prog_counter(self):
        return self.registers[self.pc_loc]

    @prog_counter.setter
    def prog_counter(self, value):
        self.registers[self.pc_loc] = value

    def step_prog(self):
        cur_run = self.prog_counter
        if 0 <= cur_run < len(self.program):
            self.func_by_name(*self.program[cur_run])
            self.prog_counter += 1
            return True
        return False


def parse_input(instruction_list):
    program = []
    jump_reg = int(instruction_list[0][-1])
    for line in instruction_list[1:]:
        op_name, *reg = line.split()
        reg = [int(i) for i in reg]
        program.append(Cmd(op_name, *reg))
    return jump_reg, program


def part_1(proc):
    proc.registers = [0] * 6

    while proc.step_prog():
        # print(proc.prog_counter, proc.registers)
        pass
    return proc.registers[0]


def part_2(proc):
    def factors(n):
        # https://stackoverflow.com/a/6800214/1038644
        return set(reduce(list.__add__, ([i, n // i] for i in range(1, int(n ** 0.5) + 1) if n % i == 0)))

    proc.registers = [0] * 6
    proc.registers[0] = 1

    while proc.step_prog():
        # print(proc.prog_counter, proc.registers)
        if proc.prog_counter == 1:
            big_num = max(proc.registers)
            return sum(factors(big_num))


if __name__ == "__main__":
    processor = Day19Processor(*parse_input(DATA.split("\n")))
    print(part_1(processor))
    print(part_2(processor))
