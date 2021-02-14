from enum import Enum
from pathlib import Path
from typing import Sequence as Seq, List, Tuple

from day02 import Processor, ProgramHalt

INPUT_FILE = Path(__file__).with_suffix(".input")


class ParamTypes(Enum):
    OP = 0
    READ = 1
    WRITE = 2


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

    def _parse_modes(self, ip: int, opcodes: Tuple[ParamTypes, ...]) -> Tuple[int, ...]:
        op, *params = self.memory[ip : ip + len(opcodes)]
        for i, val in enumerate(params):
            if opcodes[i + 1] != ParamTypes.READ:
                continue
            mode = op % (10 ** (i + 3)) // (10 ** (i + 2))
            params[i] = val if mode == 1 else self.memory[val]
        return params

    def op_add(self, ip: int) -> int:
        _opcodes = (ParamTypes.OP, ParamTypes.READ, ParamTypes.READ, ParamTypes.WRITE)
        a, b, r = self._parse_modes(ip, _opcodes)
        self.memory[r] = a + b
        return ip + len(_opcodes)

    def op_mul(self, ip: int) -> int:
        _opcodes = (ParamTypes.OP, ParamTypes.READ, ParamTypes.READ, ParamTypes.WRITE)
        a, b, r = self._parse_modes(ip, _opcodes)
        self.memory[r] = a * b
        return ip + len(_opcodes)

    def op_input(self, ip: int) -> int:
        _opcodes = (ParamTypes.OP, ParamTypes.WRITE)
        (r,) = self._parse_modes(ip, _opcodes)
        self.memory[r] = self.input.pop(0)
        return ip + len(_opcodes)

    def op_output(self, ip: int) -> int:
        _opcodes = (ParamTypes.OP, ParamTypes.READ)
        (r,) = self._parse_modes(ip, _opcodes)
        self.output.append(r)
        return ip + len(_opcodes)

    def op_jit(self, ip: int) -> int:
        _opcodes = (ParamTypes.OP, ParamTypes.READ, ParamTypes.READ)
        con, to = self._parse_modes(ip, _opcodes)
        if con == 0:
            return ip + len(_opcodes)
        else:
            return to

    def op_jif(self, ip: int) -> int:
        _opcodes = (ParamTypes.OP, ParamTypes.READ, ParamTypes.READ)
        con, to = self._parse_modes(ip, _opcodes)
        if con != 0:
            return ip + len(_opcodes)
        else:
            return to

    def op_lt(self, ip: int) -> int:
        _opcodes = (ParamTypes.OP, ParamTypes.READ, ParamTypes.READ, ParamTypes.WRITE)
        a, b, r = self._parse_modes(ip, _opcodes)
        self.memory[r] = 1 if a < b else 0
        return ip + len(_opcodes)

    def op_eq(self, ip: int) -> int:
        _opcodes = (ParamTypes.OP, ParamTypes.READ, ParamTypes.READ, ParamTypes.WRITE)
        a, b, r = self._parse_modes(ip, _opcodes)
        self.memory[r] = 1 if a == b else 0
        return ip + len(_opcodes)

    def func_by_instruction_pointer(self, ip: int) -> int:
        return self.func_by_num(self.memory[ip] % 100, ip)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    int_list = [int(i) for i in DATA.split(",")]

    print(D5Processor(int_list).run([1]))
    print(D5Processor(int_list).run([5]))
