from collections import defaultdict
from enum import Enum
from typing import Sequence as Seq, List, Tuple, Generator


class ProgramHalt(Exception):
    pass


class ParamTypes(Enum):
    OP = 0
    READ = 1
    WRITE = 2


class Processor:
    def __init__(self, program: List[int], overrides: Seq[Tuple[int, int]] = tuple()):
        self.memory = defaultdict(int, enumerate(program))
        self.overrides(overrides)
        self.mapping = {
            1: self.op_add,
            2: self.op_mul,
            3: self.op_input,
            4: self.op_output,
            5: self.op_jit,
            6: self.op_jif,
            7: self.op_lt,
            8: self.op_eq,
            9: self.op_rel_base,
            99: self.op_halt,
        }
        self.input = []
        self.output = []
        self.rel_base = 0

    def overrides(self, overrides: Seq[Tuple[int, int]]) -> None:
        for loc, val in overrides:
            self.memory[loc] = val

    def run_no_io(self) -> int:
        ip = 0
        try:
            while True:
                ip = self.func_by_instruction_pointer(ip)
        except ProgramHalt:
            return self.memory[0]

    def run(self, input_queue: List[int]) -> List[int]:
        self.input.extend(input_queue)
        ip = 0
        try:
            while True:
                ip = self.func_by_instruction_pointer(ip)
        except ProgramHalt:
            return self.output

    def run_on_output_generator(self, phase: int) -> Generator[int, int, None]:
        ip = 0
        self.input.append(phase)
        first_input = yield
        self.input.append(first_input)
        try:
            while True:
                ip = self.func_by_instruction_pointer(ip)
                if self.output:
                    new_input = yield self.output.pop(0)
                    self.input.append(new_input)
        except ProgramHalt:
            return None

    def _parse_modes(self, ip: int, opcodes: Tuple[ParamTypes, ...]) -> List[int]:
        op = self.memory[ip]
        params = []
        for i, optype in enumerate(opcodes[1:]):
            mode = op % (10 ** (i + 3)) // (10 ** (i + 2))
            val = self.memory[ip + i + 1]
            if optype == ParamTypes.WRITE:
                if mode == 2:
                    params.append(val + self.rel_base)
                else:
                    params.append(val)
            elif optype == ParamTypes.READ:
                if mode == 1:
                    params.append(val)
                elif mode == 2:
                    params.append(self.memory[val + self.rel_base])
                else:
                    params.append(self.memory[val])
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

    def op_rel_base(self, ip: int) -> int:
        _opcodes = (ParamTypes.OP, ParamTypes.READ)
        (rb,) = self._parse_modes(ip, _opcodes)
        self.rel_base += rb
        return ip + len(_opcodes)

    def op_halt(self, _):
        _opcode_length = 1
        raise ProgramHalt()

    def func_by_num(self, op_num: int, ip: int) -> int:
        assert self.mapping
        return self.mapping[op_num](ip)

    def func_by_instruction_pointer(self, ip: int) -> int:
        return self.func_by_num(self.memory[ip] % 100, ip)
