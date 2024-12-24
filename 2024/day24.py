from ast import literal_eval
from pathlib import Path

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
    results = "0b" + "".join(
        str(int(w.state))
        for w in sorted(wires.values(), key=lambda x: x.name, reverse=True)
        if w.name.startswith("z")
    )
    return literal_eval(results)


def reset_wires(wires: list[Wire]):
    for wire in wires:
        wire.state = 0
        wire.ready = False


def set_int(wires: list[Wire], val: int):
    for i, wire in enumerate(reversed(wires)):
        wire.state = ((1 << i) & val) == 1 << i
        wire.ready = True


def read_int(wires: list[Wire]):
    assert all(w.ready for w in wires)
    return int("".join(str(int(w.state)) for w in wires), 2)


def print_next_failure(sorted_wires, x_wires, y_wires, z_wires):
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
                print(
                    f"x {i=} {x:b} {x=} y {y:b} {y=} {x+y:b} {try_i:b} {x+y=} {try_i=}"
                )
                return


def part2(wires: dict[str, Wire]):
    sorted_wires = list(sorted(wires.values(), key=lambda x: x.name, reverse=True))
    x_wires = list(w for w in sorted_wires if w.name.startswith("x"))
    y_wires = list(w for w in sorted_wires if w.name.startswith("y"))
    z_wires = list(w for w in sorted_wires if w.name.startswith("z"))
    for i in range(2 ** len(x_wires)):
        reset_wires(sorted_wires)
        set_int(x_wires, 0)
        set_int(y_wires, i)
        for w in x_wires + y_wires:
            for g in w.out_gates:
                g.run()
        try_i = read_int(z_wires)
        if i != try_i:
            print(f"x_wires {i:b} {try_i:b} {i=} {try_i=}")
            break
    z09 = wires["z09"]
    nnf = wires["nnf"]
    z09.in_gates[0].output = nnf
    nnf.in_gates[0].output = z09

    print_next_failure(sorted_wires, x_wires, y_wires, z_wires)
    print(wires["z20"].print_inputs({"vkt", "wjt", "hjp"}))
    print(wires["z21"].print_inputs({"vkt", "wjt", "hjp"}))
    x20 = wires["z20"]
    nhs = wires["nhs"]
    x20.in_gates[0].output = nhs
    nhs.in_gates[0].output = x20

    print_next_failure(sorted_wires, x_wires, y_wires, z_wires)
    print(wires["z29"].print_inputs({"cfd"}))
    print(wires["z30"].print_inputs({"jmc"}))
    print(wires["z31"].print_inputs({"fmn"}))
    kqh = wires["kqh"]
    ddn = wires["ddn"]
    kqh.in_gates[0].output = ddn
    ddn.in_gates[0].output = kqh

    print_next_failure(sorted_wires, x_wires, y_wires, z_wires)
    print(wires["z33"].print_inputs({"fnk"}))
    print(wires["z34"].print_inputs({"sdt", "fnk"}))
    print(wires["z35"].print_inputs({"sdt", "fnk"}))
    z34 = wires["z34"]
    wrc = wires["wrc"]
    z34.in_gates[0].output = wrc
    wrc.in_gates[0].output = z34

    print_next_failure(sorted_wires, x_wires, y_wires, z_wires)
    return ",".join(sorted(["wrc", "z34", "ddn", "kqh", "nhs", "z20", "nnf", "z09"]))


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    WIRES_STR, GATES_STR = DATA.split("\n\n")
    WIRES = build(WIRES_STR, GATES_STR)

    print(part1(WIRES))
    print(part2(WIRES))
