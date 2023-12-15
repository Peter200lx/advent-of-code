from pathlib import Path
from typing import List

INPUT_FILE = Path(__file__).with_suffix(".input")


def aoc_hash(instr: str) -> int:
    v = 0
    for s in instr:
        v += ord(s)
        v *= 17
        v %= 256
    return v


def part_two(cmds: List[str]):
    boxes = [{} for _ in range(256)]
    for cmd in cmds:
        if "-" in cmd:
            label = cmd.split("-", maxsplit=1)[0]
            box_id = aoc_hash(label)
            box_contents = boxes[box_id]
            box_contents.pop(label, None)
        elif "=" in cmd:
            label, val = cmd.split("=", maxsplit=1)
            box_id = aoc_hash(label)
            box_contents = boxes[box_id]
            box_contents[label] = int(val)
    return sum(
        bn * sum(ln * v for ln, v in enumerate(lenses.values(), start=1))
        for bn, lenses in enumerate(boxes, start=1)
    )


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    STRINGS = [s for s in DATA.split(",")]

    print(sum(aoc_hash(s) for s in STRINGS))

    print(part_two(STRINGS))
