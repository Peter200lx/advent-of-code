from pathlib import Path
from typing import List, Tuple

INPUT_FILE = Path(__file__).with_suffix(".input")

INTERESTING_CYCLES = [20, 60, 100, 140, 180, 220]


class Processor:
    def __init__(self, program):
        self.program = program
        self.cycle = 0
        self.reg = 1
        self.record: List[Tuple[int, int]] = []
        self.screen: List[str] = [" "] * 240

    def inc_cycle(self):
        cycle_pos = self.cycle % 40
        self.cycle += 1
        if self.reg - 1 <= cycle_pos <= self.reg + 1:
            self.screen[self.cycle] = "#"
        if self.cycle in INTERESTING_CYCLES:
            self.record.append((self.cycle, self.reg))

    def display(self):
        for chunk in (
            slice(1, 41),
            slice(41, 81),
            slice(81, 121),
            slice(121, 161),
            slice(161, 201),
            slice(201, 241),
        ):
            print("".join(self.screen[chunk]))

    def op_addx(self, param):
        self.inc_cycle()
        self.inc_cycle()
        self.reg += param

    def op_noop(self, _param):
        self.inc_cycle()

    def run(self):
        for op, param in self.program:
            func = getattr(self, f"op_{op}")
            func(int(param) if param else None)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT_DATA = [(line[0:4], line[4:]) for line in DATA.split("\n")]

    proc = Processor(INPUT_DATA)
    proc.run()
    print(sum(x * y for x, y in proc.record))
    proc.display()
