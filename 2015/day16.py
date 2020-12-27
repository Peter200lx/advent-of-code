import re
from pathlib import Path
from typing import Dict

FILE_DIR = Path(__file__).parent

RE_NUMS = re.compile(r"-?\d+")

MFCSAM_TEXT = """children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1"""
MFCSAM = {k: int(v) for line in MFCSAM_TEXT.split("\n") for k, v in [line.split(": ")]}


def parse_input(input_text: str) -> Dict[int, Dict[str, int]]:
    all_aunts = {}
    for line in input_text.split("\n"):
        aunt, metadata = line.split(": ", 1)
        aunt_num = int(aunt.split()[-1])
        all_aunts[aunt_num] = {k: int(v) for element in metadata.split(", ") for k, v in [element.split(": ")]}
    return all_aunts


def part_2(aunts: Dict[int, Dict[str, int]]) -> int:
    for aunt, prop in aunts.items():
        valid = True
        for key in prop:
            if key in ("cats", "trees"):
                if MFCSAM[key] >= prop[key]:
                    valid = False
            elif key in ("pomeranians", "goldfish"):
                if MFCSAM[key] <= prop[key]:
                    valid = False
            else:
                if MFCSAM[key] != prop[key]:
                    valid = False
        if valid:
            return aunt
    raise NotImplementedError("At least 1 aunt should match the rules")


if __name__ == "__main__":
    DATA = (FILE_DIR / "day16.input").read_text().strip()
    AUNTS = parse_input(DATA)
    print([aunt for aunt, prop in AUNTS.items() if all(prop[k] == MFCSAM[k] for k in prop)][0])
    print(part_2(AUNTS))
