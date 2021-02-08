from pathlib import Path

import day12

FILE_DIR = Path(__file__).parent


class Processor(day12.Processor):
    program = None

    def o_tgl(self, x):
        tgl_line = self.pc + self._read_name_or_value(x)
        if not 0 <= tgl_line < len(self.program):
            return 1
        line = self.program[tgl_line]
        if len(line) == 2:
            if line[0] == "inc":
                line[0] = "dec"
            else:
                line[0] = "inc"
        elif len(line) == 3:
            if line[0] == "jnz":
                line[0] = "cpy"
            else:
                line[0] = "jnz"
        return 1

    def o_nop(self):
        return 1

    def o_mul(self, x, y):
        self._write_name(y, self._read_name_or_value(x) * self._read_name_or_value(y))
        return 1

    def o_add(self, x, y):
        self._write_name(y, self._read_name_or_value(x) + self._read_name_or_value(y))
        return 1

    def run_program(self, program):
        self.program = program
        self.pc = 0
        while 0 <= self.pc < len(self.program):
            try:
                self.pc += self._op_cache[self.program[self.pc][0]](*self.program[self.pc][1:])
            except TypeError:
                self.pc += 1


if __name__ == '__main__':
    DATA = (FILE_DIR / "day23.input").read_text().strip()
    proc = Processor([7, 0, 0, 0])
    proc.run_program(day12.parse_data(DATA))
    print(proc.registers[0])
    INSTRUCTIONS = day12.parse_data(DATA)
    # for i, line in enumerate(INSTRUCTIONS):
    #     print(i, " ".join(str(x) for x in line))
    INSTRUCTIONS[2] = ["mul", "b", "a"]
    for i in range(3, 10):
        INSTRUCTIONS[i] = ["nop"]
    INSTRUCTIONS[21] = ["add", "d", "a"]
    INSTRUCTIONS[22] = ["nop"]
    INSTRUCTIONS[23] = ["nop"]
    proc.registers = [12, 0, 0, 0]
    proc.run_program(INSTRUCTIONS)
    print(proc.registers[0])
