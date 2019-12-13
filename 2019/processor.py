from collections import defaultdict
from enum import Enum
from typing import Sequence as Seq, List, Tuple, Generator, NamedTuple, Optional


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
    sig: Tuple[ParamTypes, ...]

    @property
    def params(self):
        return self.sig[1:]

    @property
    def length(self):
        return len(self.sig)


OPCODES = [
    OpCode(
        1,
        "add",
        "Add two numbers",
        (ParamTypes.OP, ParamTypes.READ, ParamTypes.READ, ParamTypes.WRITE),
    ),
    OpCode(
        2,
        "mul",
        "Multiply two numbers",
        (ParamTypes.OP, ParamTypes.READ, ParamTypes.READ, ParamTypes.WRITE),
    ),
    OpCode(
        3,
        "input",
        "Read from input queue and write to destination",
        (ParamTypes.OP, ParamTypes.WRITE),
    ),
    OpCode(
        4,
        "output",
        "Read from target memory and write to output queue",
        (ParamTypes.OP, ParamTypes.READ),
    ),
    OpCode(
        5,
        "jit",
        "If first parameter is not zero set instruction pointer to second parameter",
        (ParamTypes.OP, ParamTypes.READ, ParamTypes.READ),
    ),
    OpCode(
        6,
        "jif",
        "If first parameter is zero set instruction pointer to second parameter",
        (ParamTypes.OP, ParamTypes.READ, ParamTypes.READ),
    ),
    OpCode(
        7,
        "lt",
        "If first parameter is less than second parameter, write 1 to third (else write 0)",
        (ParamTypes.OP, ParamTypes.READ, ParamTypes.READ, ParamTypes.WRITE),
    ),
    OpCode(
        8,
        "eq",
        "If first parameter is equal to second parameter, write 1 to third (else write 0)",
        (ParamTypes.OP, ParamTypes.READ, ParamTypes.READ, ParamTypes.WRITE),
    ),
    OpCode(
        9,
        "rel_base",
        "Set the processor's relative base value from parameter",
        (ParamTypes.OP, ParamTypes.READ),
    ),
    OpCode(99, "halt", "Halt the processor", (ParamTypes.OP,),),
]
OPCODE_BY_ID = {o.id: o for o in OPCODES}


class Processor:
    def __init__(
        self,
        program: List[int],
        overrides: Seq[Tuple[int, int]] = tuple(),
        *,
        debug: int = 0,
    ):
        self.memory = defaultdict(int, enumerate(program))
        self.overrides(overrides)
        self.input = []
        self.output = []
        self.rel_base = 0
        self.debug = debug
        self.mapping = {o.id: getattr(self, f"op_{o.name}") for o in OPCODES}

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

    def run_on_output_generator(
        self, phase: Optional[int] = None, output_batch: int = 1
    ) -> Generator[List[int], int, None]:
        ip = 0
        if phase is not None:
            self.input.append(phase)
        first_input = yield
        if self.debug:
            print(f"{id(self)} received {first_input} from yield")
        self.input.append(first_input)
        try:
            while True:
                ip = self.func_by_instruction_pointer(ip)
                if len(self.output) == output_batch:
                    if self.debug:
                        print(f"{id(self)} yielding out {self.output}")
                    new_input = yield self.output
                    self.output.clear()
                    if self.debug:
                        print(f"{id(self)} received {new_input} from yield")
                    self.input.append(new_input)
        except ProgramHalt:
            return None

    def run_on_input_generator(self) -> Generator[List[int], int, None]:
        ip = 0
        try:
            while True:
                if self.memory[ip] % 10 == 3:  # If next instruction is input...
                    if self.debug:
                        print(f"{id(self)} yielding out {self.output}")
                    next_input = yield self.output
                    if self.debug:
                        print(f"{id(self)} received {next_input} from yield")
                    self.output.clear()
                    self.input.append(next_input)

                ip = self.func_by_instruction_pointer(ip)
        except ProgramHalt:
            if self.output:
                if self.debug:
                    print(f"{id(self)} yielding out {self.output} before ending")
                yield self.output
            return None

    def op_add(self, a: int, b: int, r: int) -> None:
        self.memory[r] = a + b

    def op_mul(self, a: int, b: int, r: int) -> None:
        self.memory[r] = a * b

    def op_input(self, r: int) -> None:
        self.memory[r] = self.input.pop(0)

    def op_output(self, r: int) -> None:
        self.output.append(r)

    def op_jit(self, condition: int, jumpto: int) -> Optional[int]:
        if condition:
            return jumpto

    def op_jif(self, condition: int, jumpto: int) -> Optional[int]:
        if not condition:
            return jumpto

    def op_lt(self, a: int, b: int, r: int) -> None:
        self.memory[r] = 1 if a < b else 0

    def op_eq(self, a: int, b: int, r: int) -> None:
        self.memory[r] = 1 if a == b else 0

    def op_rel_base(self, rb: int) -> None:
        self.rel_base += rb

    def op_halt(self):
        raise ProgramHalt()

    def _parse_modes(self, ip: int) -> List[int]:
        raw_op = self.memory[ip]
        opcode = OPCODE_BY_ID[raw_op % 100]
        params = []
        for i, optype in enumerate(opcode.params, start=1):
            mode = raw_op % (10 ** (i + 2)) // (10 ** (i + 1))
            val = self.memory[ip + i]
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

    def _parse_modes_debug(self, ip: int) -> Tuple[List[int], str]:
        raw_op = self.memory[ip]
        opcode = OPCODE_BY_ID[raw_op % 100]
        params = []
        debug_strs = []
        for i, optype in enumerate(opcode.params, start=1):
            mode = raw_op % (10 ** (i + 2)) // (10 ** (i + 1))
            val = self.memory[ip + i]
            if optype == ParamTypes.WRITE:
                if mode == 2:
                    params.append(val + self.rel_base)
                    debug_strs.append(f"vREL({val:`>3})")
                else:
                    params.append(val)
                    debug_strs.append(f"vPOS({val:`>3})")
            elif optype == ParamTypes.READ:
                if mode == 1:
                    params.append(val)
                    debug_strs.append(f"^IMM({val:`>3})")
                elif mode == 2:
                    params.append(self.memory[val + self.rel_base])
                    debug_strs.append(f"^REL({val:`>3})")
                else:
                    params.append(self.memory[val])
                    debug_strs.append(f"^POS({val:`>3})")
        if self.debug >= 2:
            debug_strs = [f"{s}={params[i]:<4}" for i, s in enumerate(debug_strs)]
        return params, " ".join(debug_strs)

    def func_by_instruction_pointer(self, ip: int) -> int:
        opcode = OPCODE_BY_ID[self.memory[ip] % 100]
        if self.debug >= 1:
            parameters, param_str = self._parse_modes_debug(ip)
            print(
                f"{ip:05} {f'{self.rel_base:5} ' if self.rel_base else ''}"
                f"{opcode.name:^8} {self.memory[ip]:5} {param_str}"
            )
        else:
            parameters = self._parse_modes(ip)
        new_ip = self.mapping[opcode.id](*parameters)
        return new_ip if new_ip is not None else ip + opcode.length
