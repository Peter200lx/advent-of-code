from itertools import combinations
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


class Comp:
    def __init__(self, name):
        self.name = name
        self.connections = set()


def build(lines: list[str]):
    computers = {}
    for line in lines:
        first, second = line.split("-")
        if first not in computers:
            computers[first] = Comp(first)
        if second not in computers:
            computers[second] = Comp(second)
        computers[first].connections.add(computers[second])
        computers[second].connections.add(computers[first])
    return computers


def part1(computers: dict[str, Comp]) -> set[frozenset[[Comp]]]:
    sets = set()
    for comp in (c for n, c in computers.items() if n.startswith("t")):
        for a, b in combinations(comp.connections, 2):
            if a in b.connections:
                sets.add(frozenset((comp, a, b)))
    return sets


def part2(triples: set[frozenset[[Comp]]]) -> str:
    big_sets = []
    for tri_group in triples:
        a, b, c = list(tri_group)
        a_set = a.connections | {a}
        b_set = b.connections | {b}
        c_set = c.connections | {c}
        big_sets.append(a_set & b_set & c_set)
    for valid_set in sorted(big_sets, key=lambda x: len(x), reverse=True):
        if any(a not in b.connections for a, b in combinations(valid_set, 2)):
            continue
        return ",".join(c.name for c in sorted(valid_set, key=lambda x: x.name))


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    LINES = list(DATA.split("\n"))
    COMPUTERS = build(LINES)

    THREE_PAIRS = part1(COMPUTERS)
    print(len(THREE_PAIRS))
    print(part2(THREE_PAIRS))
