from collections import defaultdict
from enum import Enum
from typing import Sequence as Seq, List, Tuple, Generator, NamedTuple, Callable


class ProgramHalt(Exception):
    pass


class ParamTypes(Enum):
    OP = 0
    READ = 1
    WRITE = 2


class OpCode(NamedTuple):
    id: int
    name: str
    description: str
    func: Callable
    sig: Tuple[ParamTypes, ...]

    @property
    def params(self):
        return self.sig[1:]


class Processor:
    def __init__(self, program: List[int], overrides: Seq[Tuple[int, int]] = tuple()):
        self.memory = defaultdict(int, enumerate(program))
        self.overrides(overrides)
        self.input = []
        self.output = []
        self.rel_base = 0
        self.mapping = {
            1: OpCode(
                1,
                "add",
                "Add two numbers",
                self.op_add,
                (ParamTypes.OP, ParamTypes.READ, ParamTypes.READ, ParamTypes.WRITE),
            ),
            2: OpCode(
                2,
                "mul",
                "Multiply two numbers",
                self.op_mul,
                (ParamTypes.OP, ParamTypes.READ, ParamTypes.READ, ParamTypes.WRITE),
            ),
            3: OpCode(
                3,
                "input",
                "Read from input queue and write to destination",
                self.op_input,
                (ParamTypes.OP, ParamTypes.WRITE),
            ),
            4: OpCode(
                4,
                "output",
                "Read from target memory and write to output queue",
                self.op_output,
                (ParamTypes.OP, ParamTypes.READ),
            ),
            5: OpCode(
                5,
                "jit",
                "If first parameter is not zero set instruction pointer to second parameter",
                self.op_jit,
                (ParamTypes.OP, ParamTypes.READ, ParamTypes.READ),
            ),
            6: OpCode(
                6,
                "jif",
                "If first parameter is zero set instruction pointer to second parameter",
                self.op_jif,
                (ParamTypes.OP, ParamTypes.READ, ParamTypes.READ),
            ),
            7: OpCode(
                7,
                "lt",
                "If first parameter is less than second parameter, write 1 to third (else write 0)",
                self.op_lt,
                (ParamTypes.OP, ParamTypes.READ, ParamTypes.READ, ParamTypes.WRITE),
            ),
            8: OpCode(
                8,
                "eq",
                "If first parameter is equal to second parameter, write 1 to third (else write 0)",
                self.op_eq,
                (ParamTypes.OP, ParamTypes.READ, ParamTypes.READ, ParamTypes.WRITE),
            ),
            9: OpCode(
                9,
                "rel_base",
                "Set the processor's relative base value from parameter",
                self.op_rel_base,
                (ParamTypes.OP, ParamTypes.READ),
            ),
            99: OpCode(
                99, "halt", "Halt the processor", self.op_halt, (ParamTypes.OP,),
            ),
        }

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

    def func_by_instruction_pointer(self, ip: int) -> int:
        opcode = self.mapping[self.memory[ip] % 100]
        return opcode.func(ip)
