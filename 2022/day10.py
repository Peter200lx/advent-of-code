from pathlib import Path
from typing import List, Tuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Processor:
    def __init__(self):
        self.cycle = 0
        self.reg = 1
        self.record: List[Tuple[int, int]] = []
        self.screen: List[str] = [" "] * 240

    def inc_cycle(self):
        if self.reg - 1 <= self.cycle % 40 <= self.reg + 1:
            self.screen[self.cycle] = "#"
        self.cycle += 1
        if self.cycle in range(20, 221, 40):
            self.record.append((self.cycle, self.reg))

    def display(self):
        for i in range(0, 241, 40):
            print("".join(self.screen[i : i + 40]))

    def op_addx(self, param):
        self.inc_cycle()
        self.inc_cycle()
        self.reg += param

    def op_noop(self, _param):
        self.inc_cycle()

    def run(self, program: List[Tuple[str, str]]):
        for op, param in program:
            func = getattr(self, f"op_{op}")
            func(int(param) if param else None)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT_DATA = [(line[0:4], line[4:]) for line in DATA.split("\n")]

    proc = Processor()
    proc.run(INPUT_DATA)
    print(sum(x * y for x, y in proc.record))
    proc.display()
