from pathlib import Path
from typing import Callable, Sequence as Seq, List, Tuple


class ProgramHalt(Exception):
    pass


class Processor:
    def __init__(self, program: List[int], overrides: Seq[Tuple[int, int]] = tuple()):
        self.memory = program[:]
        self.mapping = {1: self.op_add, 2: self.op_mul, 99: self.op_halt}
        self.overrides(overrides)

    def overrides(self, overrides: Seq[Tuple[int, int]]) -> None:
        for loc, val in overrides:
            self.memory[loc] = val

    def run(self) -> int:
        ip = 0
        try:
            while True:
                ip = self.func_by_instruction_pointer(ip)
        except ProgramHalt:
            return self.memory[0]

    def op_add(self, ip: int) -> int:
        _opcode_length = 4
        _, a, b, r = self.memory[ip : ip + _opcode_length]
        self.memory[r] = self.memory[a] + self.memory[b]
        return ip + _opcode_length

    def op_mul(self, ip: int) -> int:
        _opcode_length = 4
        _, a, b, r = self.memory[ip : ip + _opcode_length]
        self.memory[r] = self.memory[a] * self.memory[b]
        return ip + _opcode_length

    def op_halt(self, _):
        _opcode_length = 1
        raise ProgramHalt()

    @property
    def ops_list(self):
        return [
            (n[3:], getattr(self, n)) for n in self.__dir__() if n.startswith("op_")
        ]

    def _func_from_name(self, op_name: str) -> Callable[[int], int]:
        method_name = "op_" + op_name
        return getattr(self, method_name)

    def func_by_name(self, op_name: str, ip: int) -> int:
        return self._func_from_name(op_name)(ip)

    def func_by_num(self, op_num: int, ip: int) -> int:
        assert self.mapping
        return self.mapping[op_num](ip)

    def func_by_instruction_pointer(self, ip: int) -> int:
        return self.func_by_num(self.memory[ip], ip)


def find_state(list_o_codes, desired_state):
    for noun in range(100):
        for verb in range(100):
            if Processor(list_o_codes, ((1, noun), (2, verb))).run() == desired_state:
                return noun, verb


if __name__ == "__main__":
    DATA = Path("day02.input").read_text().strip()
    int_list = [int(i) for i in DATA.split(",")]

    print(Processor(int_list, ((1, 12), (2, 2))).run())
    noun, verb = find_state(int_list, 19690720)
    print(noun, verb, 100 * noun + verb)
