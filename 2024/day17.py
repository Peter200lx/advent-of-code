from pathlib import Path
from typing import Optional

INPUT_FILE = Path(__file__).with_suffix(".input")


class Comp:
    def __init__(self, data: str):
        a_str, b_str, c_str, _blank, prog_str = data.split("\n")
        self.a = int(a_str.split()[-1])
        self.b = int(b_str.split()[-1])
        self.c = int(c_str.split()[-1])
        self.prog = [int(n) for n in prog_str.split()[-1].split(",")]
        self.insts = [
            self.adv,
            self.bxl,
            self.bst,
            self.jnz,
            self.bxc,
            self.out,
            self.bdv,
            self.cdv,
        ]
        self.output = []

    def adv(self, val: int):
        self.a //= 2 ** self._calc_combo(val)

    def bxl(self, val: int):
        self.b ^= val

    def bst(self, val: int):
        self.b = self._calc_combo(val) % 8

    def jnz(self, val: int) -> Optional[int]:
        if self.a != 0:
            return val

    def bxc(self, val: int):
        self.b ^= self.c

    def out(self, val: int):
        self.output.append(self._calc_combo(val) % 8)

    def bdv(self, val: int):
        self.b = self.a // (2 ** self._calc_combo(val))

    def cdv(self, val: int):
        self.c = self.a // (2 ** self._calc_combo(val))

    def _calc_combo(self, val: int) -> int:
        if 0 <= val <= 3:
            return val
        elif val == 4:
            return self.a
        elif val == 5:
            return self.b
        elif val == 6:
            return self.c
        else:
            raise NotImplemented

    def __repr__(self):
        return f"Comp({self.a=}, {self.b=}, {self.c=}, {self.prog=})"

    def run(self):
        cur_op = 0
        while cur_op < len(self.prog):
            op, val = self.prog[cur_op : cur_op + 2]
            new_op = self.insts[op](val)
            if new_op is not None:
                cur_op = new_op
            else:
                cur_op += 2


def part2_first(data: str) -> int:
    for i in range(999999999999):
        comp = Comp(data)
        comp.a = i
        comp.run()
        print(i, comp.output)


def part2_maybe_smarter(prog: list[int]) -> int:
    for i in range(8 ** (len(prog) - 1), 8 ** (len(prog) + 1)):
        test = []
        while i:
            val = (i % 8) ^ (i >> ((i % 8) ^ 7))
            test.append(val)
            i //= 8
        if test == prog:
            return i


def p2_test(data: str, start: int, length: int) -> list[int]:
    res = []
    for j in range(8):
        comp = Comp(data)
        comp.a = start + j
        comp.run()
        if comp.output == comp.prog[-length - 1 :]:
            res.append(start + j)
    return res


def part2(data: str, prog: list[int]) -> int:
    viable = [0]
    for i in range(len(prog)):
        viable = [r for n in viable for r in p2_test(data, n << 3, i)]
    return min(viable)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    COMPUTER = Comp(DATA)

    COMPUTER.run()
    print(",".join(str(n) for n in COMPUTER.output))
    print(part2(DATA, COMPUTER.prog))
