from collections import defaultdict
from pathlib import Path
from typing import List, Tuple

from day05 import D5Processor, ParamTypes


class D9Processor(D5Processor):
    def __init__(self, program: List[int]):
        self.memory = defaultdict(int)
        self.memory.update(enumerate(program))
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

    def _parse_modes(self, ip: int, opcodes: Tuple[ParamTypes, ...]) -> List[int]:
        op = self.memory[ip]
        params = [self.memory[i] for i in range(ip + 1, ip + len(opcodes))]
        for i, val in enumerate(params):
            mode = op % (10 ** (i + 3)) // (10 ** (i + 2))
            if opcodes[i + 1] == ParamTypes.WRITE:
                if mode == 2:
                    params[i] = val + self.rel_base
                else:
                    params[i] = val
                continue
            if mode == 1:
                params[i] = val
            elif mode == 2:
                params[i] = self.memory[val + self.rel_base]
            else:
                params[i] = self.memory[val]
        return params

    def op_rel_base(self, ip: int) -> int:
        _opcodes = (ParamTypes.OP, ParamTypes.READ)
        (rb,) = self._parse_modes(ip, _opcodes)
        self.rel_base += rb
        return ip + len(_opcodes)


if __name__ == "__main__":
    DATA = Path("day09.input").read_text().strip()
    int_list = [int(i) for i in DATA.split(",")]

    print(D9Processor(int_list).run([1]))
    print(D9Processor(int_list).run([2]))
