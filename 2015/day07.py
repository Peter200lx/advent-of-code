from pathlib import Path
from typing import Union, Dict, Optional

INPUT_FILE = Path(__file__).with_suffix(".input")


class Operation:
    def __init__(self, instructions: Dict[str, "Operation"], myid: str, a: Union[str, int]):
        self._a = a
        self._a_value: Optional[int] = None
        self._override: Optional[int] = None
        self.id = myid
        self.inst = instructions

    def override(self, value: int):
        self._override = value

    @property
    def a(self) -> int:
        if self._a_value is None:
            self._a_value = self.inst[self._a].calc() if isinstance(self._a, str) else self._a
        return self._a_value

    def calc(self) -> int:
        if self._override is not None:
            return self._override
        return self._calc()

    def _calc(self) -> int:
        return self.a


class Invert(Operation):
    def _calc(self):
        return ~self.a


class And(Operation):
    def __init__(self, instructions: Dict[str, "Operation"], myid: str, a: Union[str, int], b: Union[str, int]):
        self._b = b
        self._b_value: Optional[int] = None
        super().__init__(instructions, myid, a)

    @property
    def b(self) -> int:
        if self._b_value is None:
            self._b_value = self.inst[self._b].calc() if isinstance(self._b, str) else self._b
        return self._b_value

    def _calc(self) -> int:
        return self.a & self.b


class Or(And):
    def _calc(self) -> int:
        return self.a | self.b


class LShift(And):
    def _calc(self) -> int:
        return self.a << self.b


class RShift(And):
    def _calc(self) -> int:
        return self.a >> self.b


OPS_2 = {" AND ": And, " OR ": Or, " LSHIFT ": LShift, " RSHIFT ": RShift}


def int_or_str(value: str) -> Union[str, int]:
    try:
        return int(value)
    except ValueError:
        return value


def parse_line(lines: str) -> Dict[str, Operation]:
    instructions = {}
    for line in lines.split("\n"):
        in_op, out = line.split(" -> ")
        for key in OPS_2:
            if key in in_op:
                a, b = in_op.split(key)
                instructions[out] = OPS_2[key](instructions, out, int_or_str(a), int_or_str(b))
                break
        else:
            if "NOT" in in_op:
                _, a = in_op.split("NOT ")
                instructions[out] = Invert(instructions, out, int_or_str(a))
            else:
                instructions[out] = Operation(instructions, out, int_or_str(in_op))
    return instructions


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    CIRCUIT = parse_line(DATA)
    part_1 = CIRCUIT["a"].calc()
    print(part_1)
    CIRCUIT_2 = parse_line(DATA)
    CIRCUIT_2["b"].override(part_1)
    print(CIRCUIT_2["a"].calc())
