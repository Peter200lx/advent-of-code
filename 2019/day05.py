from pathlib import Path
from typing import Sequence as Seq, List, Tuple, Set

from day02 import Processor, ProgramHalt


class D5Processor(Processor):
    def __init__(self, program: List[int], overrides: Seq[Tuple[int, int]] = tuple()):
        super(D5Processor, self).__init__(program, overrides)
        self.mapping = {
            1: self.op_add,
            2: self.op_mul,
            3: self.op_input,
            4: self.op_output,
            5: self.op_jit,
            6: self.op_jif,
            7: self.op_lt,
            8: self.op_eq,
            99: self.op_halt,
        }
        self.input = []
        self.output = []

    def run(self, input_queue: List[int]) -> List[int]:
        self.input.extend(input_queue)
        ip = 0
        try:
            while True:
                ip = self.func_by_instruction_pointer(ip)
        except ProgramHalt:
            return self.output

    def _parse_modes(self, ip: int, op_len: int, imm_mode: Set[int] = None) -> Tuple[int, ...]:
        op, *params = self.memory[ip : ip + op_len]
        for i, val in enumerate(params):
            if imm_mode and i in imm_mode:
                continue
            mode = op % (10 ** (i + 3)) // (10 ** (i + 2))
            params[i] = val if mode == 1 else self.memory[val]
        return params

    def op_add(self, ip: int) -> int:
        _opcode_length = 4
        a, b, r = self._parse_modes(ip, _opcode_length, {2})
        self.memory[r] = a + b
        return ip + _opcode_length

    def op_mul(self, ip: int) -> int:
        _opcode_length = 4
        a, b, r = self._parse_modes(ip, _opcode_length, {2})
        self.memory[r] = a * b
        return ip + _opcode_length

    def op_input(self, ip: int) -> int:
        _opcode_length = 2
        (r,) = self._parse_modes(ip, _opcode_length, {0})
        self.memory[r] = self.input.pop()
        return ip + _opcode_length

    def op_output(self, ip: int) -> int:
        _opcode_length = 2
        (r,) = self._parse_modes(ip, _opcode_length)
        self.output.append(r)
        return ip + _opcode_length

    def op_jit(self, ip: int) -> int:
        _opcode_length = 3
        con, to = self._parse_modes(ip, _opcode_length)
        if con == 0:
            return ip + _opcode_length
        else:
            return to

    def op_jif(self, ip: int) -> int:
        _opcode_length = 3
        con, to = self._parse_modes(ip, _opcode_length)
        if con != 0:
            return ip + _opcode_length
        else:
            return to

    def op_lt(self, ip: int) -> int:
        _opcode_length = 4
        a, b, r = self._parse_modes(ip, _opcode_length, {2})
        self.memory[r] = 1 if a < b else 0
        return ip + _opcode_length

    def op_eq(self, ip: int) -> int:
        _opcode_length = 4
        a, b, r = self._parse_modes(ip, _opcode_length, {2})
        self.memory[r] = 1 if a == b else 0
        return ip + _opcode_length

    def func_by_instruction_pointer(self, ip: int) -> int:
        return self.func_by_num(self.memory[ip] % 100, ip)


if __name__ == "__main__":
    DATA = Path("day05.input").read_text().strip()
    int_list = [int(i) for i in DATA.split(",")]

    print(D5Processor(int_list).run([1]))
    print(D5Processor(int_list).run([5]))
