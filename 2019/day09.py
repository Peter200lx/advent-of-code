from collections import defaultdict
from pathlib import Path
from typing import List, Tuple

from day05 import D5Processor, ParamTypes


class D9Processor(D5Processor):
    def __init__(self, program: List[int]):
        self.memory = defaultdict(int, enumerate(program))
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
