import subprocess
from pathlib import Path
from typing import List, Dict

INPUT_FILE = Path(__file__).with_suffix(".input")


def part_1(in_tuples: List[List[str]]) -> int:
    vars = {}
    indicies = set(range(len(in_tuples)))
    while indicies:
        for i, (var, exp) in enumerate(in_tuples):
            try:
                value = eval(str(exp), globals(), vars)
            except:
                continue
            vars[var] = value
            indicies.discard(i)
    return int(vars["root"])


def build_str(data_dict: Dict[str, str], start: str) -> str:
    if start == "humn":
        return "x"
    components = data_dict.get(start).split()
    if len(components) == 1:
        return components[0]
    elif len(components) == 3:
        return f"({build_str(data_dict, components[0])}) {components[1]} ({build_str(data_dict, components[2])})"
    raise NotImplemented


def part_2(in_tuples: List[List[str]]):
    """Need to have qalc installed and available on the CLI to run"""
    unprocessed = dict(in_tuples)
    left, _op, right = unprocessed.pop("root").split()
    unprocessed.pop("humn")
    left_full = build_str(unprocessed, left)
    right_full = build_str(unprocessed, right)
    try:
        var = eval(left_full)
        subprocess.run(["qalc", "-t", f"{var}={right_full}"])
    except:
        var = eval(right_full)
        subprocess.run(["qalc", "-t", f"{left_full}={var}"])


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    VARS = [list(line.split(": ")) for line in DATA.split("\n")]

    print(part_1(VARS))
    part_2(VARS)
