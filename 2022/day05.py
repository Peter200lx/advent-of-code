import re
from pathlib import Path
from typing import List, Dict

INPUT_FILE = Path(__file__).with_suffix(".input")

RE_NUMS = re.compile(r"-?\d+")


def parse_start(start: str) -> Dict[int, List[str]]:
    start_lines = start.split("\n")
    index_to_tower: Dict[int, int] = {}
    for i, c in enumerate(start_lines[-1]):  # find index of tower numbers
        if c.isdigit():
            index_to_tower[i] = int(c)
    row_items: Dict[int, List[str]] = {i: [] for i in index_to_tower.values()}
    for row in start_lines[-2:None:-1]:  # move up towers
        for index, val in index_to_tower.items():
            if row[index] != " ":
                row_items[val].append(row[index])
    return row_items


def run_moves_9000(start: str, moves: str) -> str:
    towers = parse_start(start)
    for line in moves.split("\n"):
        if not line:
            continue
        num, fro, to = list(map(int, RE_NUMS.findall(line)))
        for _i in range(num):
            towers[to].append(towers[fro].pop())
    return "".join(towers[c][-1] for c in sorted(towers))


def run_moves_9001(start: str, moves: str) -> str:
    towers = parse_start(start)
    for line in moves.split("\n"):
        if not line:
            continue
        num, fro, to = list(map(int, RE_NUMS.findall(line)))
        towers[fro], to_move = towers[fro][:-num], towers[fro][-num:]
        towers[to].extend(to_move)
    return "".join(towers[c][-1] for c in sorted(towers))


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    START, MOVES = DATA.split("\n\n")

    print(run_moves_9000(START, MOVES))
    print(run_moves_9001(START, MOVES))
