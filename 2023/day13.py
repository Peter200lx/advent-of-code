from pathlib import Path
from typing import NamedTuple, Optional

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int


class Pattern:
    def __init__(self, chunk: str):
        lines = chunk.strip().split("\n")
        self.rocks = set(
            Coord(x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == "#"
        )
        self.max = Coord(len(lines[0]), len(lines))
        self.matched_line = set()

    def calc_ref(self) -> int:
        return self.calc_set(self.rocks)

    def calc_smudge(self) -> int:
        for y in range(self.max.y):
            for x in range(self.max.x):
                if (x, y) in self.rocks:
                    rocks = set(self.rocks)
                    rocks.discard((x, y))
                else:
                    rocks = self.rocks | {Coord(x, y)}
                result = self.calc_set(rocks)
                if result is not None:
                    return result

    def calc_set(self, rocks) -> Optional[int]:
        col_values = []
        possible_mirror_points = []
        for col in range(self.max.x):
            col_values.append(sorted(p.y for p in rocks if p.x == col))
            if len(col_values) > 1:
                if col_values[col] == col_values[col - 1]:
                    possible_mirror_points.append(col)
        for x in possible_mirror_points:
            failed = False
            for i in range(self.max.x):
                my_coord = x + i
                other_coord = x - 1 - i
                if 0 <= other_coord and my_coord < self.max.x:
                    if col_values[my_coord] != col_values[other_coord]:
                        failed = True
                        break
            if not failed:
                key = ("C", x)
                if key in self.matched_line:
                    continue
                self.matched_line.add(key)
                return x
        row_values = []
        possible_mirror_points = []
        for row in range(self.max.y):
            row_values.append(sorted(p.x for p in rocks if p.y == row))
            if len(row_values) > 1:
                if row_values[row] == row_values[row - 1]:
                    possible_mirror_points.append(row)
        for y in possible_mirror_points:
            failed = False
            for i in range(self.max.y + 1):
                my_coord = y + i
                other_coord = y - 1 - i
                if 0 <= other_coord and my_coord < self.max.y:
                    if row_values[my_coord] != row_values[other_coord]:
                        failed = True
                        break
            if not failed:
                key = ("R", y)
                if key in self.matched_line:
                    continue
                self.matched_line.add(key)
                return 100 * y
        return None


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    PATTERNS = [Pattern(chunk) for chunk in DATA.split("\n\n")]

    print(sum(p.calc_ref() for p in PATTERNS))

    print(sum(p.calc_smudge() for p in PATTERNS))
