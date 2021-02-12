import re
from collections import namedtuple
from typing import Callable, Dict, List, Optional, Tuple

TestChange = namedtuple("TChange", ["reg_before", "op_test", "reg_after"])
RE_NUMS = re.compile(r"-?\d+")


class Processor:
    mapping: Optional[Dict[int, Callable[[int, int, int], None]]]

    def __init__(self):
        self.registers = [0] * 4
        self.mapping = None

    def _register_input(self, list_vals: List[int]) -> None:
        for val in list_vals:
            assert 0 <= val < len(self.registers)

    def op_addr(self, a, b, c):
        self._register_input([a, b, c])
        self.registers[c] = self.registers[a] + self.registers[b]

    def op_addi(self, a, b, c):
        self._register_input([a, c])
        self.registers[c] = self.registers[a] + b

    def op_mulr(self, a, b, c):
        self._register_input([a, b, c])
        self.registers[c] = self.registers[a] * self.registers[b]

    def op_muli(self, a, b, c):
        self._register_input([a, c])
        self.registers[c] = self.registers[a] * b

    def op_banr(self, a, b, c):
        self._register_input([a, b, c])
        self.registers[c] = self.registers[a] & self.registers[b]

    def op_bani(self, a, b, c):
        self._register_input([a, c])
        self.registers[c] = self.registers[a] & b

    def op_borr(self, a, b, c):
        self._register_input([a, b, c])
        self.registers[c] = self.registers[a] | self.registers[b]

    def op_bori(self, a, b, c):
        self._register_input([a, c])
        self.registers[c] = self.registers[a] | b

    def op_setr(self, a, _, c):
        self._register_input([a, c])
        self.registers[c] = self.registers[a]

    def op_seti(self, a, _, c):
        self._register_input([c])
        self.registers[c] = a

    def op_gtir(self, a, b, c):
        self._register_input([b, c])
        self.registers[c] = int(a > self.registers[b])

    def op_gtri(self, a, b, c):
        self._register_input([a, c])
        self.registers[c] = int(self.registers[a] > b)

    def op_gtrr(self, a, b, c):
        self._register_input([a, b, c])
        self.registers[c] = int(self.registers[a] > self.registers[b])

    def op_eqir(self, a, b, c):
        self._register_input([b, c])
        self.registers[c] = int(a == self.registers[b])

    def op_eqri(self, a, b, c):
        self._register_input([a, c])
        self.registers[c] = int(self.registers[a] == b)

    def op_eqrr(self, a, b, c):
        self._register_input([a, b, c])
        self.registers[c] = int(self.registers[a] == self.registers[b])

    @property
    def ops_list(self):
        return [(n[3:], getattr(self, n)) for n in self.__dir__() if n.startswith("op_")]

    def test_change(self, tchange: TestChange):
        valid_ops = set()
        old_reg = self.registers[:]
        for op_name, op_func in self.ops_list:
            self.registers = tchange.reg_before[:]
            op_func(*tchange.op_test[1:])
            if self.registers == tchange.reg_after:
                valid_ops.add(op_name)
        self.registers = old_reg
        return valid_ops

    def build_from_tests(self, tests: List[TestChange]) -> Dict[int, str]:
        possible_mapping = {}
        for test in tests:
            op_num = test.op_test[0]
            if op_num not in possible_mapping:
                possible_mapping[op_num] = self.test_change(test)
            else:
                possible_mapping[op_num] &= self.test_change(test)

        still_multiple = True
        remove_future = set()
        while still_multiple:
            still_multiple = False
            for op in sorted(possible_mapping.values(), key=lambda x: len(x)):
                if len(op) == 1:
                    remove_future |= op
                else:
                    op -= remove_future
                    if len(op) > 1:
                        still_multiple = True
        mapping = {k: tuple(v)[0] for k, v in possible_mapping.items()}
        self.mapping = {k: self._func_from_name(v) for k, v in mapping.items()}
        return mapping

    def _func_from_name(self, op_name: str) -> Callable[[int, int, int], None]:
        method_name = "op_" + op_name
        return getattr(self, method_name)

    def func_by_name(self, op_name: str, a: int, b: int, c: int) -> None:
        self._func_from_name(op_name)(a, b, c)

    def func_by_num(self, op_num: int, a: int, b: int, c: int) -> None:
        assert self.mapping
        self.mapping[op_num](a, b, c)


def parse_input(data_str: str) -> Tuple[List[TestChange], List[List[int]]]:
    test_inputs = []
    program = []
    test_strs, code_strs = data_str.split("\n\n\n")
    test_str_list = test_strs.split("\n\n")
    for test_str in test_str_list:
        begin_str, op_str, after_str = test_str.strip().split("\n")
        test_inputs.append(
            TestChange(
                list(map(int, RE_NUMS.findall(begin_str))),
                list(map(int, RE_NUMS.findall(op_str))),
                list(map(int, RE_NUMS.findall(after_str))),
            )
        )
    for code_str in code_strs.strip().split("\n"):
        op = list(map(int, RE_NUMS.findall(code_str)))
        assert len(op) == 4
        program.append(op)
    return test_inputs, program


def part_1(tests):
    processor = Processor()
    count_3_or_more = 0
    for test in tests:
        valid_ops = processor.test_change(test)
        if len(valid_ops) >= 3:
            count_3_or_more += 1
    return count_3_or_more


def part_2(tests, code):
    processor = Processor()
    processor.build_from_tests(tests)
    for op_cmd in code:
        processor.func_by_num(*op_cmd)
    return processor.registers


if __name__ == "__main__":
    with open("day16.input", "r") as in_file:
        DATA = in_file.read()

    watch_tests, watch_code = parse_input(DATA)
    print(part_1(watch_tests))
    print(part_2(watch_tests, watch_code)[0])
