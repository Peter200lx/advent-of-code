from typing import NamedTuple, Optional, Tuple

DATA = """jio a, +22
inc a
tpl a
tpl a
tpl a
inc a
tpl a
inc a
tpl a
inc a
inc a
tpl a
inc a
inc a
tpl a
inc a
inc a
tpl a
inc a
inc a
tpl a
jmp +19
tpl a
tpl a
tpl a
tpl a
inc a
inc a
tpl a
inc a
tpl a
inc a
inc a
tpl a
inc a
inc a
tpl a
inc a
tpl a
tpl a
jio a, +8
inc b
jie a, +4
tpl a
inc a
jmp +2
hlf a
jmp -7"""


class Instruction(NamedTuple):
    name: str
    reg: str = None
    offset: int = None

    @staticmethod
    def parse_line(line: str) -> "Instruction":
        name, params = line.split(maxsplit=1)
        if name == "jmp":
            return Instruction(name, offset=int(params))
        elif "," in params:
            reg, offset = params.split(", ")
            return Instruction(name, reg=reg, offset=int(offset))
        else:
            return Instruction(name, reg=params)


class Processor:
    def __init__(self, program: Tuple[Instruction]):
        self.program = program
        self.reg = {"a": 0, "b": 0}
        self.mapping = {m[3:]: getattr(self, m) for m in dir(self) if m.startswith("op_")}

    def op_hlf(self, inst: Instruction) -> None:
        self.reg[inst.reg] //= 2

    def op_tpl(self, inst: Instruction) -> None:
        self.reg[inst.reg] *= 3

    def op_inc(self, inst: Instruction) -> None:
        self.reg[inst.reg] += 1

    def op_jmp(self, inst: Instruction) -> int:
        return inst.offset

    def op_jie(self, inst: Instruction) -> Optional[int]:
        if self.reg[inst.reg] % 2 == 0:
            return inst.offset

    def op_jio(self, inst: Instruction) -> Optional[int]:
        if self.reg[inst.reg] == 1:
            return inst.offset

    def run(self):
        ip = 0
        while 0 <= ip < len(self.program):
            inst = self.program[ip]
            new_ip = self.mapping[inst.name](inst)
            ip += 1 if new_ip is None else new_ip
        return self.reg["b"]


if __name__ == "__main__":
    INST = tuple(Instruction.parse_line(inst) for inst in DATA.split("\n"))
    proc = Processor(INST)
    print(proc.run())
    proc.reg = {"a": 1, "b": 0}
    print(proc.run())
