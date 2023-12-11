from pathlib import Path
from typing import NamedTuple, Set, Tuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int

    def manh(self, other: "Coord") -> int:
        return abs(other.x - self.x) + abs(other.y - self.y)


def load_galaxies(instr: str) -> Tuple[Set[Coord], Set[Coord]]:
    galaxies = {
        Coord(x, y)
        for y, line in enumerate(instr.split("\n"))
        for x, c in enumerate(line)
        if c == "#"
    }
    gal_x, gal_y = {c.x for c in galaxies}, {c.y for c in galaxies}
    minx, maxx = min(c.x for c in galaxies), max(c.x for c in galaxies)
    miny, maxy = min(c.y for c in galaxies), max(c.y for c in galaxies)
    empty_columns = {n for n in range(minx, maxx + 1) if n not in gal_x}
    empty_rows = {n for n in range(miny, maxy + 1) if n not in gal_y}
    p1_gal = set()
    p2_gal = set()
    p1_row_add = p2_row_add = 0
    for y in range(miny, maxy + 1):
        if y in empty_rows:
            p1_row_add += 1
            p2_row_add += 1000000 - 1
            continue
        p1_col_add = p2_col_add = 0
        for x in range(minx, maxx + 1):
            if x in empty_columns:
                p1_col_add += 1
                p2_col_add += 1000000 - 1
                continue
            if (x, y) in galaxies:
                p1_gal.add(Coord(x + p1_col_add, y + p1_row_add))
                p2_gal.add(Coord(x + p2_col_add, y + p2_row_add))
    return p1_gal, p2_gal


def solve(galaxies: Set[Coord]) -> int:
    processed = set(galaxies)
    manhs = 0
    while processed:
        next_gal = processed.pop()
        for other_gal in processed:
            manhs += next_gal.manh(other_gal)
    return manhs


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    P1_GAL, P2_GAL = load_galaxies(DATA)

    print(solve(P1_GAL))
    print(solve(P2_GAL))
