from pathlib import Path
from typing import List, NamedTuple, Optional, Set

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

    def part_one(self) -> int:
        return self.calc_set(self.rocks)

    def calc_smudge(self) -> int:
        for y in range(self.max.y):
            for x in range(self.max.x):
                if (x, y) in self.rocks:
                    result = self.calc_set(self.rocks - {(x, y)})
                else:
                    result = self.calc_set(self.rocks | {Coord(x, y)})
                if result is not None:
                    return result

    def calc_slices(self, key: str, slices: List[List[int]], max_n: int) -> Optional[int]:
        for n in range(1, max_n):
            failed = False
            for i in range(max_n):
                my_coord = n + i
                other_coord = n - 1 - i
                if 0 <= other_coord and my_coord < max_n:
                    if slices[my_coord] != slices[other_coord]:
                        failed = True
                        break
                else:
                    break
            if not failed:
                my_key = (key, n)
                if my_key in self.matched_line:
                    continue
                self.matched_line.add(my_key)
                return n
        return None

    def calc_set(self, rocks: Set[Coord]) -> Optional[int]:
        col_values = [sorted(p.y for p in rocks if p.x == col) for col in range(self.max.x)]
        ret = self.calc_slices("C", col_values, self.max.x)
        if ret is not None:
            return ret
        row_values = [sorted(p.x for p in rocks if p.y == row) for row in range(self.max.y)]
        ret = self.calc_slices("R", row_values, self.max.y)
        if ret is not None:
            return 100 * ret
        return ret


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    PATTERNS = [Pattern(chunk) for chunk in DATA.split("\n\n")]

    print(sum(p.part_one() for p in PATTERNS))

    print(sum(p.calc_smudge() for p in PATTERNS))
