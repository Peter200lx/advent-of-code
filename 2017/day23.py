from collections import defaultdict
from typing import List, Optional

DATA = """set b 93
set c b
jnz a 2
jnz 1 5
mul b 100
sub b -100000
set c b
sub c -17000
set f 1
set d 2
set e 2
set g d
mul g e
sub g b
jnz g 2
set f 0
sub e -1
set g e
sub g b
jnz g -8
sub d -1
set g d
sub g b
jnz g -13
jnz f 2
sub h -1
set g b
sub g c
jnz g 2
jnz 1 3
sub b -17
jnz 1 -23"""


class Program(object):
    def __init__(self, inst_list: List[str]):
        self.registers = defaultdict(int)
        # self.registers['a'] = 1
        self.inst_list = inst_list
        self.prog_counter = 0
        self.mul_count = 0

    def get_value(self, reg_or_val: str) -> int:
        try:
            return int(reg_or_val)
        except ValueError:
            return self.registers[reg_or_val]

    def i_set(self, x_val: str, y_val: str) -> None:
        self.registers[x_val] = self.get_value(y_val)

    def i_sub(self, x_val: str, y_val: str) -> None:
        self.registers[x_val] -= self.get_value(y_val)

    def i_mul(self, x_val: str, y_val: str) -> None:
        self.registers[x_val] *= self.get_value(y_val)
        self.mul_count += 1

    def i_jnz(self, x_val: str, y_val: str) -> Optional[int]:
        if self.get_value(x_val) != 0:
            return self.get_value(y_val)
        else:
            return None

    def run_insts(self):
        while 0 <= self.prog_counter < len(self.inst_list):
            inst = self.inst_list[self.prog_counter].split()
            result = getattr(self, 'i_' + inst[0])(*inst[1:])
            if result is not None:
                self.prog_counter += result
            else:
                self.prog_counter += 1


def part_two() -> int:
    h_count = 0
    b = 109300  # 93 * 100 + 100000
    c = b + 17000
    while b <= c:
        found = False
        d = 2
        while d != b:
            # Following three lines are new code replacing commented out code
            if b % d == 0:
                found = True
                break
            # e = 2
            # while e != b:
            #     if d * e == b:
            #         found = True
            #     e += 1
            d += 1
        if found:
            h_count += 1
        b += 17
    return h_count


if __name__ == '__main__':
    prog = Program([s for s in DATA.split('\n')])
    prog.run_insts()
    print(prog.mul_count)
    print(part_two())
