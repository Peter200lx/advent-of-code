from pathlib import Path
from typing import Optional

INPUT_FILE = Path(__file__).with_suffix(".input")


class Wire:
    def __init__(self, name: str, state=None):
        self.name = name
        if state is not None:
            self.state = bool(int(state))
            self.ready = True
        else:
            self.state = None
            self.ready = False
        self.in_gates: list[Gate] = []
        self.out_gates: list[Gate] = []

    def __repr__(self):
        return f"Wire({self.name}, {self.state=} {self.ready=})"

    def print_inputs(self, skip: set[str]):
        if self.name in skip:
            return f"{self.name}(SKIP)"
        assert len(self.in_gates) in {0, 1}, f"{len(self.in_gates)}"
        if self.in_gates:
            return f"{self.name}({self.in_gates[0].print_inputs(skip)})"
        else:
            return f"{self.name}"

    def get_inputs(self, skip: set[str]) -> list[str]:
        if self.name in skip:
            return []
        if not self.in_gates:
            return [self.name]
        return [self.name] + self.in_gates[0].get_inputs(skip)


class Gate:
    def __init__(self, line: str):
        from_str, self.wire_out_str = line.split(" -> ")
        w_in_1, self.gate_type, w_in_2 = from_str.split()
        self.wire_in_strs = (w_in_1, w_in_2)
        self.input = []
        self.output: Wire = None

    def run(self):
        if not all(w.ready for w in self.input):
            return
        if self.output.ready:
            return
        if self.gate_type == "AND":
            self.output.state = self.input[0].state & self.input[1].state
        elif self.gate_type == "OR":
            self.output.state = self.input[0].state | self.input[1].state
        elif self.gate_type == "XOR":
            self.output.state = self.input[0].state ^ self.input[1].state
        self.output.ready = True
        for gate in self.output.out_gates:
            gate.run()

    def print_inputs(self, skip: set[str]):
        return f"{self.input[0].print_inputs(skip)} {self.gate_type} {self.input[1].print_inputs(skip)}"

    def get_inputs(self, skip: set[str]) -> list[str]:
        return self.input[0].get_inputs(skip) + self.input[1].get_inputs(skip)


def build(wires_str: str, gates_str: str):
    wires = {}
    for line in wires_str.split("\n"):
        name, state = line.split(": ")
        wire = Wire(name, state)
        wires[wire.name] = wire
    for line in gates_str.split("\n"):
        gate = Gate(line)
        if gate.wire_out_str not in wires:
            wires[gate.wire_out_str] = Wire(gate.wire_out_str)
        wires[gate.wire_out_str].in_gates.append(gate)
        gate.output = wires[gate.wire_out_str]
        for in_w in gate.wire_in_strs:
            if in_w not in wires:
                wires[in_w] = Wire(in_w)
            wires[in_w].out_gates.append(gate)
            gate.input.append(wires[in_w])
    return wires


def part1(wires: dict[str, Wire]):
    for wire in (w for w in wires.values() if w.ready):
        for gate in wire.out_gates:
            gate.run()
    results = "".join(
        str(int(w.state))
        for w in sorted(wires.values(), key=lambda x: x.name, reverse=True)
        if w.name.startswith("z")
    )
    return int(results, 2)


def reset_wires(wires: list[Wire]):
    for wire in wires:
        wire.state = 0
        wire.ready = False


def set_int(wires: list[Wire], val: int):
    for i, wire in enumerate(reversed(wires)):
        wire.state = ((1 << i) & val) == 1 << i
        wire.ready = True


def read_int(wires: list[Wire]):
    if not all(w.ready for w in wires):
        raise ValueError(f"Not all wires are ready to read")
    return int("".join(str(int(w.state)) for w in wires), 2)


def print_next_failure(sorted_wires, x_wires, y_wires, z_wires) -> Optional[int]:
    for i in range(1, len(x_wires)):
        for x, y in ((2**i, 0), (0, 2**i), (2**i, 2**i)):
            reset_wires(sorted_wires)
            set_int(x_wires, x)
            set_int(y_wires, y)
            for w in x_wires + y_wires:
                for g in w.out_gates:
                    g.run()
            try_i = read_int(z_wires)
            if x + y != try_i:
                # print(
                #     f"x {i=} {x:b} {x=} y {y:b} {y=} {x+y:b} {try_i:b} {x+y=} {try_i=}"
                # )
                return i + 1 if x and y else i
    return None


def part2(wires: dict[str, Wire]):
    sorted_wires = list(sorted(wires.values(), key=lambda x: x.name, reverse=True))
    x_wires = list(w for w in sorted_wires if w.name.startswith("x"))
    y_wires = list(w for w in sorted_wires if w.name.startswith("y"))
    z_wires = list(w for w in sorted_wires if w.name.startswith("z"))

    found_strs = []
    failure_index = print_next_failure(sorted_wires, x_wires, y_wires, z_wires)
    while True:
        found = False
        # We can ignore all wires that were involved in the solution above the problem area
        ignore_wires = {
            w.name for w in wires[f"z{failure_index-1:02}"].in_gates[0].input
        }
        for first in wires[f"z{failure_index:02}"].get_inputs(ignore_wires):
            for second in wires[f"z{failure_index+1:02}"].get_inputs(ignore_wires):
                f_wire, s_wire = wires[first], wires[second]
                if not f_wire.in_gates or not s_wire.in_gates:
                    continue
                # print(f"Trying {first=} {second=}")
                f_wire.in_gates[0].output = s_wire
                s_wire.in_gates[0].output = f_wire
                try:
                    next_index = print_next_failure(
                        sorted_wires, x_wires, y_wires, z_wires
                    )
                except ValueError:
                    f_wire.in_gates[0].output = f_wire
                    s_wire.in_gates[0].output = s_wire
                    continue
                if next_index is None:
                    # print(first, second)
                    found_strs += [first, second]
                    return ",".join(sorted(found_strs))
                elif next_index > failure_index + 1:
                    if (
                        first.startswith("z")
                        and len(set(s_wire.get_inputs(ignore_wires))) > 9
                    ):
                        # When ignoring wires in one level up, 9 is how many inputs this level should have
                        # print(f"Bad {first=} {second=}, {len(set(s_wire.get_inputs(ignore_wires)))=}")
                        f_wire.in_gates[0].output = f_wire
                        s_wire.in_gates[0].output = s_wire
                        continue
                    # print(first, second)
                    found_strs += [first, second]
                    found = True
                    failure_index = next_index
                    break
                f_wire.in_gates[0].output = f_wire
                s_wire.in_gates[0].output = s_wire
            if found:
                break


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    WIRES_STR, GATES_STR = DATA.split("\n\n")
    WIRES = build(WIRES_STR, GATES_STR)

    print(part1(WIRES))
    print(part2(WIRES))
