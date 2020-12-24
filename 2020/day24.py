from pathlib import Path
from typing import Set, NamedTuple

FILE_DIR = Path(__file__).parent


class HexCoord(NamedTuple):
    r"""
     /\/\/\/\/\
    |0|1|2|3|4| odd rows
    \/\/\/\/\/\
    |0|1|2|3|4| even rows
    \/\/\/\/\/\
    |1|2|3|4|5| odd rows
    \/\/\/\/\/
    """
    row: int
    col: int

    def __add__(self, other):
        return HexCoord(self.row + other.row, self.col + other.col)


MOVES = {
    "e": lambda row: HexCoord(0, 1),
    "se": lambda row: HexCoord(-1, 1) if row % 2 == 0 else HexCoord(-1, 0),
    "sw": lambda row: HexCoord(-1, 0) if row % 2 == 0 else HexCoord(-1, -1),
    "w": lambda row: HexCoord(0, -1),
    "nw": lambda row: HexCoord(1, 0) if row % 2 == 0 else HexCoord(1, -1),
    "ne": lambda row: HexCoord(1, 1) if row % 2 == 0 else HexCoord(1, 0),
}


def find_point(line: str) -> HexCoord:
    cur_point = HexCoord(0, 0)
    i = 0
    while i < len(line):
        if line[i] in MOVES:
            direction = MOVES[line[i]](cur_point.row)
            i += 1
        else:
            direction = MOVES[line[i : i + 2]](cur_point.row)
            i += 2
        cur_point += direction
    return cur_point


def generate_start(all_lines: str) -> Set[HexCoord]:
    all_points = set()
    for line in all_lines.split("\n"):
        next_point = find_point(line)
        if next_point in all_points:
            all_points.discard(next_point)
        else:
            all_points.add(next_point)
    return all_points


def calc_point(floor: Set[HexCoord], position: HexCoord) -> bool:
    is_black = position in floor
    adjacent_count = sum((position + d(position.row)) in floor for d in MOVES.values())
    if is_black:
        if adjacent_count == 0 or adjacent_count > 2:
            return False
        return True
    elif not is_black and adjacent_count == 2:
        return True
    return False


def run_life_again(start: Set[HexCoord]) -> int:
    current_map = start
    for _ in range(100):
        possible_spaces = {p + d(p.row) for d in MOVES.values() for p in current_map}
        current_map = {p for p in possible_spaces if calc_point(current_map, p)}
    return len(current_map)


if __name__ == "__main__":
    DATA = (FILE_DIR / "day24.input").read_text().strip()
    STARTING_MAP = generate_start(DATA)
    print(len(STARTING_MAP))
    print(run_life_again(STARTING_MAP))
