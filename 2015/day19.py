import re
from collections import defaultdict
from pathlib import Path
from typing import Set, Tuple, Dict

FILE_DIR = Path(__file__).parent


def parse_input(input_text: str) -> Tuple[Dict[str, Set[str]], str]:
    rules = defaultdict(set)
    rules_str, start_molecule = input_text.split("\n\n")
    for line in rules_str.split("\n"):
        replace, to = line.split(" => ")
        rules[replace].add(to)
    return dict(rules), start_molecule


def possible_next(rules: Dict[str, Set[str]], start_molecule: str) -> Set[str]:
    possible = set()
    for replace, replacements in rules.items():
        for match in re.finditer(replace, start_molecule):
            for new_seq in replacements:
                possible.add(start_molecule[: match.start()] + new_seq + start_molecule[match.end() :])
    return possible


def build_mol(rules: Dict[str, Set[str]], start_molecule: str):
    reversed_rules = {rep: orig for orig, reps in rules.items() for rep in reps}
    sorted_rules = sorted(reversed_rules.items(), key=lambda x: len(x[0]), reverse=True)
    new_str = start_molecule
    steps = 0
    while new_str != "e":
        for from_str, to in sorted_rules:
            match = re.search(from_str, new_str)
            if match:
                new_str = new_str[: match.start()] + to + new_str[match.end() :]
                break
        steps += 1
    return steps


if __name__ == "__main__":
    DATA = (FILE_DIR / "day19.input").read_text().strip()
    RULES, START_MOL = parse_input(DATA)
    print(len(possible_next(RULES, START_MOL)))
    print(build_mol(RULES, START_MOL))
