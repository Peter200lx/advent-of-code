import re
from pathlib import Path
from typing import List, Dict

INPUT_FILE = Path(__file__).with_suffix(".input")

RE_NUMS = re.compile(r"-?\d+")


def parse_start(start: str) -> Dict[int, List[str]]:
    start_lines = start.split("\n")
    row_pas: Dict[int, int] = {}
    for i, c in enumerate(start_lines[-1]):
        if c.isdigit():
            row_pas[i] = int(c)
    row_items: Dict[int, List[str]] = {i: list() for i in row_pas.values()}
    for row in start_lines[-2:None:-1]:
        if not row:
            continue
        for index, val in row_pas.items():
            if row[index] != " ":
                row_items[val].append(row[index])
    return row_items


def run_moves_9000(start: str, moves: str) -> str:
    towers = parse_start(start)
    for move in moves.split("\n"):
        if not move:
            continue
        num, fro, to = list(map(int, RE_NUMS.findall(move)))
        assert len(towers[fro]) >= num
        for _i in range(num):
            towers[to].append(towers[fro].pop())
    return "".join(towers[c][-1] for c in sorted(towers))


def run_moves_9001(start: str, moves: str) -> str:
    towers = parse_start(start)
    for move in moves.split("\n"):
        if not move:
            continue
        num, fro, to = list(map(int, RE_NUMS.findall(move)))
        assert len(towers[fro]) >= num
        moved = towers[fro][-num:]
        towers[fro] = towers[fro][:-num]
        towers[to].extend(moved)
    return "".join(towers[c][-1] for c in sorted(towers))


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    START, MOVES = DATA.split("\n\n")

    print(run_moves_9000(START, MOVES))
    print(run_moves_9001(START, MOVES))
