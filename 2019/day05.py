from pathlib import Path
from typing import Callable, Sequence as Seq, List, Tuple


class ProgramHalt(Exception):
    pass


class Processor:
    def __init__(self, program: List[int], overrides: Seq[Tuple[int, int]] = tuple()):
        self.memory = program[:]
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
        self.overrides(overrides)
        self.input = []
        self.output = []

    def overrides(self, overrides: Seq[Tuple[int, int]]) -> None:
        for loc, val in overrides:
            self.memory[loc] = val

    def run(self, input_queue):
        self.input.extend(input_queue)
        ip = 0
        try:
            while True:
                ip = self.func_by_instruction_pointer(ip)
        except ProgramHalt:
            return self.output

    def op_add(self, ip: int) -> int:
        _opcode_length = 4
        op, a, b, r = self.memory[ip : ip + _opcode_length]
        amode = op % 1000 // 100
        bmode = op % 10000 // 1000
        a_val = a if amode == 1 else self.memory[a]
        b_val = b if bmode == 1 else self.memory[b]
        self.memory[r] = a_val + b_val
        return ip + _opcode_length

    def op_mul(self, ip: int) -> int:
        _opcode_length = 4
        op, a, b, r = self.memory[ip : ip + _opcode_length]
        amode = op % 1000 // 100
        bmode = op % 10000 // 1000
        a_val = a if amode == 1 else self.memory[a]
        b_val = b if bmode == 1 else self.memory[b]
        self.memory[r] = a_val * b_val
        return ip + _opcode_length

    def op_input(self, ip: int):
        _opcode_length = 2
        _, r = self.memory[ip : ip + _opcode_length]
        self.memory[r] = self.input.pop()
        return ip + _opcode_length

    def op_output(self, ip: int):
        _opcode_length = 2
        op, r = self.memory[ip : ip + _opcode_length]
        rmode = op % 1000 // 100
        r_val = r if rmode == 1 else self.memory[r]
        self.output.append(r_val)
        return ip + _opcode_length

    def op_jit(self, ip: int):
        _opcode_length = 3
        op, con, to = self.memory[ip : ip + _opcode_length]
        con_mode = op % 1000 // 100
        to_mode = op % 10000 // 1000
        con_val = con if con_mode == 1 else self.memory[con]
        to_val = to if to_mode == 1 else self.memory[to]
        if con_val == 0:
            return ip + _opcode_length
        else:
            return to_val

    def op_jif(self, ip: int):
        _opcode_length = 3
        op, con, to = self.memory[ip : ip + _opcode_length]
        con_mode = op % 1000 // 100
        to_mode = op % 10000 // 1000
        con_val = con if con_mode == 1 else self.memory[con]
        to_val = to if to_mode == 1 else self.memory[to]
        if con_val != 0:
            return ip + _opcode_length
        else:
            return to_val

    def op_lt(self, ip: int):
        _opcode_length = 4
        op, a, b, r = self.memory[ip : ip + _opcode_length]
        amode = op % 1000 // 100
        bmode = op % 10000 // 1000
        a_val = a if amode == 1 else self.memory[a]
        b_val = b if bmode == 1 else self.memory[b]
        self.memory[r] = 1 if a_val < b_val else 0
        return ip + _opcode_length

    def op_eq(self, ip: int):
        _opcode_length = 4
        op, a, b, r = self.memory[ip : ip + _opcode_length]
        amode = op % 1000 // 100
        bmode = op % 10000 // 1000
        a_val = a if amode == 1 else self.memory[a]
        b_val = b if bmode == 1 else self.memory[b]
        self.memory[r] = 1 if a_val == b_val else 0
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
        return self.func_by_num(self.memory[ip] % 100, ip)


if __name__ == "__main__":
    DATA = Path("day05.input").read_text().strip()
    int_list = [int(i) for i in DATA.split(",")]

    print(Processor(int_list).run([1]))
    print(Processor(int_list).run([5]))
