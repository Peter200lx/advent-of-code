from pathlib import Path
from typing import List, Tuple

INPUT_FILE = Path(__file__).with_suffix(".input")


def part_one(components: List[Tuple[str, Tuple[str, ...]]]) -> int:
    nodes = {name: set(right) for name, right in components}
    nodes.update(
        {name: set() for _left, right in components for name in right if name not in nodes}
    )
    for left, right in components:
        for item in right:
            nodes[item].add(left)

    start_node = max(nodes, key=lambda x: len(nodes[x]))
    building_set = {start_node}
    next_set = set(nodes[start_node])
    while len(next_set) != 3:
        all_considered = building_set | next_set
        to_add = min(next_set, key=lambda x: sum(v not in all_considered for v in nodes[x]))
        next_set.remove(to_add)
        building_set.add(to_add)
        next_set |= nodes[to_add] - building_set
    return len(building_set) * len(nodes.keys() - building_set)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    COMPONENTS = [
        (left, tuple(right.split()))
        for line in DATA.split("\n")
        for left, right in [line.split(": ")]
    ]

    print(part_one(COMPONENTS))
