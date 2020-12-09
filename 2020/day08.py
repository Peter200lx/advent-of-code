from pathlib import Path
from typing import List, NamedTuple

FILE_DIR = Path(__file__).parent


class Instruction(NamedTuple):
    op: str
    value: int

    def invert(self):
        if self.op == "jmp":
            return Instruction("nop", self.value)
        elif self.op == "nop":
            return Instruction("jmp", self.value)
        else:
            return self


class Processor:
    def __init__(self, program: List[Instruction]):
        self.program = program
        self.acc = 0
        self.mapping = {m[3:]: getattr(self, m) for m in dir(self) if m.startswith("op_")}

    def op_acc(self, value: int) -> None:
        self.acc += value

    def op_jmp(self, value: int) -> int:
        return value

    def op_nop(self, _value) -> None:
        pass

    def run(self):
        ip = 0
        visited_ip = set()
        while ip not in visited_ip:
            visited_ip.add(ip)
            ip = self.func_by_instruction_pointer(ip, self.program[ip])
            if ip >= len(self.program):
                return True
        return False

    def func_by_instruction_pointer(self, ip, inst: Instruction) -> int:
        new_ip = self.mapping[inst.op](inst.value)
        return ip + (1 if new_ip is None else new_ip)


def part_2(instructions: List[Instruction]):
    for i in range(len(instructions)):
        if instructions[i].op == "acc":
            continue
        my_inst = instructions.copy()
        my_inst[i] = instructions[i].invert()
        proc = Processor(my_inst)
        if proc.run():
            print(i, instructions[i])
            print(proc.acc)
            break


if __name__ == "__main__":
    DATA = (FILE_DIR / "day08.input").read_text().strip()
    INST = [Instruction(op, int(val)) for inst in DATA.split("\n") for op, val in [inst.split()]]
    part_1 = Processor(INST)
    part_1.run()
    print(part_1.acc)
    part_2(INST)
