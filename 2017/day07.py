import re
from collections import Counter
from typing import List, Dict
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

EXAMPLE_DATA = """pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)"""


class Tower:
    def __init__(self, name: str, weight: int, chld_str_list: List[str]):
        self.name = name
        self.weight = weight
        self.chld_str_list = chld_str_list
        self.children = []
        self.parent = None

    def add_child(self, tower: "Tower"):
        self.children.append(tower)

    def add_parent(self, tower: "Tower"):
        assert self.parent is None
        self.parent = tower

    def child_weights(self) -> int:
        if not self.children:
            return self.weight
        child_weights = []
        for child in self.children:
            child_weights.append(child.child_weights())
        count = Counter(child_weights).most_common()
        if len(count) > 1:
            proper_value, odd_value = count
            odd_child = self.children[child_weights.index(odd_value[0])]
            print(f"I am {self.name}, bad child is {odd_child.name} who weighs {odd_child.weight} by themselves")
            print(f"child_weights {child_weights}")
            print(f"{odd_child.name} should weigh: {odd_child.weight + (proper_value[0] - odd_value[0])}  <--- 2")
            child_weights[child_weights.index(odd_value[0])] = proper_value[0]
        return self.weight + sum(child_weights)


def initialize_towers(commands: List[str]) -> Dict[str, Tower]:
    struct = {}
    line_regex = re.compile(r"([a-z]+) \((\d+)\)(?: -> ([a-z]+(?:, [a-z]+)*))?")
    for command in commands:
        name, weight, children = line_regex.findall(command)[0]
        struct[name] = Tower(name, int(weight), [i.strip() for i in children.split(",") if i.strip()])
    return struct


def link_towers(struct: Dict[str, Tower]):
    for pos_parent in struct:
        if struct[pos_parent].chld_str_list:
            for child in struct[pos_parent].chld_str_list:
                struct[pos_parent].add_child(struct[child])
                struct[child].add_parent(struct[pos_parent])


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INSTRUCTIONS = [line for line in DATA.split("\n")]

    structure = initialize_towers(INSTRUCTIONS)
    link_towers(structure)
    for linked_tower in structure.values():
        if linked_tower.parent is None:
            print(f"Name of head: {linked_tower.name}  <--- 1")
            print(f"Total weight of structure {linked_tower.child_weights()}")
