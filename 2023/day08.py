import re
from math import lcm
from pathlib import Path
from typing import Dict

INPUT_FILE = Path(__file__).with_suffix(".input")

RE_NUMS = re.compile(r"-?\d+")


class Node:
    def __init__(self, name: str, left: str, right: str):
        self.id = name
        self.left_str = left
        self.right_str = right
        self.left = None
        self.right = None

    def __repr__(self):
        return f"Node({self.id}, {self.left_str=} {self.right_str=})"


def parse_input(instr: str):
    dirs, nodestr = instr.split("\n\n")
    nodes = {}
    for line in nodestr.split("\n"):
        name, items = line.split(" = ")
        left_name, right_name = items.strip("()").split(", ")
        nodes[name] = Node(name, left_name, right_name)
    for node in nodes.values():
        node.left = nodes[node.left_str]
        node.right = nodes[node.right_str]
    return dirs, nodes


def part_one(path: str, nodes):
    steps = 0
    found = False
    start = nodes["AAA"]
    next_node = start
    while True:
        for c in path:
            if c == "L":
                next_node = next_node.left
            elif c == "R":
                next_node = next_node.right
            steps += 1
            if next_node.id == "ZZZ":
                found = True
                break
        if found:
            break
    return steps


def part_two(path: str, nodes: Dict[str, Node]):
    steps = 0
    found = False
    starts = [n for n in nodes.values() if n.id.endswith("A")]
    cur_nodes = list(starts)
    repeat = [None] * len(cur_nodes)
    seen = [{} for _ in repeat]
    while True:
        for c in path:
            if c == "L":
                cur_nodes = [n.left for n in cur_nodes]
            elif c == "R":
                cur_nodes = [n.right for n in cur_nodes]
            steps += 1
            for i, node in enumerate(cur_nodes):
                if not node.id.endswith("Z"):
                    continue
                if node.id in seen[i] and not repeat[i]:
                    repeat[i] = seen[i][node.id]
                    continue
                seen[i][node.id] = steps
            if all(repeat):
                found = True
                break
        if found:
            break
    return lcm(*repeat)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    DIRS, NODES = parse_input(DATA)

    print(part_one(DIRS, NODES))

    print(part_two(DIRS, NODES))
