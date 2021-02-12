from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


def parse_data(program):
    parsed_prog = []
    for i, line in enumerate(program.split("\n")):
        parsed_prog.append([])
        for item in line.split():
            try:
                item = int(item)
            except ValueError:
                pass
            parsed_prog[i].append(item)
    return parsed_prog


class Processor:
    def __init__(self, starting_reg=None):
        self.pc = 0
        self.registers = starting_reg if starting_reg else [0] * 4
        self._op_cache = {k[2:]: getattr(self, k) for k in dir(self) if k.startswith("o_")}

    def _read_name_or_value(self, x):
        if isinstance(x, str):
            return self.registers[ord(x) - ord("a")]
        else:
            return x

    def _write_name(self, x, value):
        self.registers[ord(x) - ord("a")] = value

    def o_cpy(self, x, y):
        self._write_name(y, self._read_name_or_value(x))
        return 1

    def o_inc(self, x):
        self._write_name(x, self._read_name_or_value(x) + 1)
        return 1

    def o_dec(self, x):
        self._write_name(x, self._read_name_or_value(x) - 1)
        return 1

    def o_jnz(self, x, y):
        if self._read_name_or_value(x) == 0:
            return 1
        else:
            return self._read_name_or_value(y)

    def run_program(self, program):
        while 0 <= self.pc < len(program):
            self.pc += self._op_cache[program[self.pc][0]](*program[self.pc][1:])


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INSTRUCTIONS = parse_data(DATA)
    proc = Processor()
    proc.run_program(INSTRUCTIONS)
    print(proc.registers[0])
    p2_proc = Processor([0, 0, 1, 0])
    p2_proc.run_program(INSTRUCTIONS)
    print(p2_proc.registers[0])
