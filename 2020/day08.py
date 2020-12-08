from pathlib import Path
from typing import List, Tuple

FILE_DIR = Path(__file__).parent


class Processor:
    def __init__(
        self,
        program: List[Tuple[str, int]],
    ):
        self.program = program
        self.acc = 0
        self.mapping = {m[3:]: getattr(self, m) for m in dir(self) if m.startswith("op_")}

    def op_acc(self, a: int) -> None:
        self.acc += a

    def op_jmp(self, a: int) -> int:
        return a

    def op_nop(self, a: int) -> None:
        pass

    def run(self):
        ip = 0
        visited_ip = set()
        while ip not in visited_ip:
            visited_ip.add(ip)
            op, v = self.program[ip]
            ip = self.func_by_instruction_pointer(ip, op, v)
            if ip >= len(self.program):
                return True
        return False

    def func_by_instruction_pointer(self, ip, op: str, a: int) -> int:
        new_ip = self.mapping[op](a)
        return ip + new_ip if new_ip is not None else ip + 1


def part_2(instructions):
    for i in range(len(instructions)):
        if instructions[i][0] == "acc":
            continue
        my_inst = instructions.copy()
        if instructions[i][0] == "jmp":
            my_inst[i] = ("nop", instructions[i][1])
        elif instructions[i][0] == "nop":
            my_inst[i] = ("jmp", instructions[i][1])
        proc = Processor(my_inst)
        if proc.run():
            print(i, instructions[i])
            print(proc.acc)
            break


if __name__ == "__main__":
    DATA = (FILE_DIR / "day08.input").read_text().strip()
    INST = [(op, int(val)) for inst in DATA.split("\n") for op, val in [inst.split()]]
    part_1 = Processor(INST)
    part_1.run()
    print(part_1.acc)
    part_2(INST)