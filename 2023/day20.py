from collections import deque
from enum import Enum
from math import prod
from pathlib import Path
from typing import Dict, List, NamedTuple, Set, Tuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Pulse(Enum):
    low = 0
    high = 1

    def inv(self) -> "Pulse":
        return Pulse.high if self is Pulse.low else Pulse.low


class Signal(NamedTuple):
    source: str
    target: str
    pulse: Pulse

    def __repr__(self):
        return f"{self.source} -{self.pulse}> {self.target}"


class Module:
    def __init__(self, line: str):
        self.name, rest = line.split(" -> ")
        self.outputs = [s for s in rest.split(", ")]
        self.inputs = []

    def init(self):
        pass

    def recv(self, signal: Signal) -> List[Signal]:
        return [Signal(self.name, s, signal.pulse) for s in self.outputs]


class FlipFlop(Module):
    def __init__(self, line: str):
        super().__init__(line[1:])
        self.state = Pulse.low

    def init(self):
        self.state = Pulse.low

    def recv(self, signal: Signal) -> List[Signal]:
        if signal.pulse is Pulse.high:
            return []
        self.state = self.state.inv()
        return [Signal(self.name, s, self.state) for s in self.outputs]


class Conj(Module):
    def __init__(self, line: str):
        super().__init__(line[1:])
        self.in_states: Dict[str, Pulse] = {}

    def init(self):
        self.in_states = {s: Pulse.low for s in self.inputs}

    def recv(self, signal: Signal) -> List[Signal]:
        assert signal.source in self.in_states
        self.in_states[signal.source] = signal.pulse
        if all(p is Pulse.high for p in self.in_states.values()):
            to_send = Pulse.low
        else:
            to_send = Pulse.high
        return [Signal(self.name, s, to_send) for s in self.outputs]


class RatsNest:
    def __init__(self, instr: str):
        self.modules: Dict[str, Module] = {}
        for line in instr.split("\n"):
            if line.startswith("%"):
                mod = FlipFlop(line)
                self.modules[mod.name] = mod
            elif line.startswith("&"):
                mod = Conj(line)
                self.modules[mod.name] = mod
            else:
                mod = Module(line)
                self.modules[mod.name] = mod
        for mod in self.modules.values():
            for out in mod.outputs:
                if out not in self.modules:
                    continue
                self.modules[out].inputs.append(mod.name)
        for mod in self.modules.values():
            mod.init()

        self.p2_sources = {}

    def press_button(self, loop: int = 0) -> Tuple[int, int]:
        lows = highs = 0
        queue = deque([Signal("button", "broadcaster", Pulse.low)])
        while queue:
            cur: Signal = queue.popleft()
            # print(cur)
            if cur.pulse == Pulse.low:
                lows += 1
            else:
                highs += 1
            if cur.source in self.p2_sources and cur.pulse is Pulse.high:
                if not self.p2_sources[cur.source]:
                    self.p2_sources[cur.source] = loop
            if cur.target not in self.modules:
                continue
            for sig in self.modules[cur.target].recv(cur):
                queue.append(sig)
        # print(f"{self.lows=}, {self.highs=}, {self.lows*self.highs}")
        return lows, highs

    def find_useful(self, nodes: Set[str]):
        to_add = {i for m in nodes for i in self.modules[m].inputs if i not in nodes}
        while to_add:
            nodes |= to_add
            to_add = {i for m in nodes for i in self.modules[m].inputs if i not in nodes}
        return nodes

    def run_p2(self):
        final = None
        for mod in self.modules.values():
            mod.init()
            if "rx" in mod.outputs:
                final = mod
        assert isinstance(final, Conj)
        full_modules = self.modules
        self.modules = {m: self.modules[m] for m in self.find_useful(set(final.inputs))}
        self.p2_sources = {n: 0 for n in final.inputs}
        for i in range(1, 9999999999):
            self.press_button(i)
            if all(self.p2_sources.values()):
                return prod(self.p2_sources.values())
        self.modules = full_modules


def part_one(ratsnest: RatsNest) -> int:
    lows = highs = 0
    for _ in range(1000):
        nl, nh = ratsnest.press_button()
        lows += nl
        highs += nh
    return lows * highs


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    RATSNEST = RatsNest(DATA)

    print(part_one(RATSNEST))
    print(RATSNEST.run_p2())
