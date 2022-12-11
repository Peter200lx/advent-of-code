import re
import math
from pathlib import Path
from typing import Dict, List, Optional

INPUT_FILE = Path(__file__).with_suffix(".input")
RE_NUMS = re.compile(r"-?\d+")


class Monkey:
    def __init__(self, to_parse: str, num: int):
        lines = to_parse.split("\n")
        self.id = int(RE_NUMS.findall(lines[0])[0])
        assert self.id == num
        self.starting_items = tuple(map(int, RE_NUMS.findall(lines[1])))
        self.op_str = lines[2][23]
        try:
            self.op_right = int(lines[2][24:])
        except ValueError:
            self.op_right = None
        self.div_by = int(RE_NUMS.findall(lines[3])[0])
        self.if_true = int(RE_NUMS.findall(lines[4])[0])
        self.if_false = int(RE_NUMS.findall(lines[5])[0])
        self.items: List[int] = []
        self.inspect_count = 0

    def reset(self):
        self.items = list(self.starting_items)
        self.inspect_count = 0

    def turn(self, all_monkeys: Dict[int, "Monkey"], lcm: Optional[int]):
        for item in self.items:
            self.inspect_count += 1
            right = self.op_right or item
            if self.op_str == "*":
                item *= right
            elif self.op_str == "+":
                item += right
            else:
                raise NotImplementedError
            if lcm:
                item %= lcm
            else:
                item = int(item / 3)
            if item % self.div_by == 0:
                all_monkeys[self.if_true].items.append(item)
            else:
                all_monkeys[self.if_false].items.append(item)
        self.items = []


def run_game(monkeys: Dict[int, Monkey], p2=False):
    all(m.reset() for m in monkeys.values())
    lcm = math.lcm(*(m.div_by for m in monkeys.values())) if p2 else None
    for i in range(10_000 if p2 else 20):
        for monkey in monkeys.values():
            monkey.turn(monkeys, lcm)
    totals = [monkey.inspect_count for monkey in monkeys.values()]
    totals.sort(reverse=True)
    return totals[0] * totals[1]


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT_DATA = {i: Monkey(section, i) for i, section in enumerate(DATA.split("\n\n"))}

    print(run_game(INPUT_DATA))
    print(run_game(INPUT_DATA, p2=True))
