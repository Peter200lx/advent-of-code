from pathlib import Path
from typing import NamedTuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)


# fmt: off
dirs = [Coord(-1, -1), Coord(0, -1), Coord(1, -1),
        Coord(-1, 0),                Coord(1, 0),
        Coord(-1, 1),  Coord(0, 1),  Coord(1, 1)]
# fmt: on


def p1(field: set[Coord]) -> set[Coord]:
    return {c for c in field if sum(c + d in field for d in dirs) < 4}


def p2(field: set[Coord]) -> int:
    changed = True
    remove_count = 0
    while changed:
        to_remove = p1(field)
        remove_count += len(to_remove)
        new_field = field - to_remove
        changed = len(field) != len(new_field)
        field = new_field
    return remove_count


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    FIELD = {
        Coord(x, y)
        for y, line in enumerate(DATA.split("\n"))
        for x, c in enumerate(line)
        if c == "@"
    }

    print(len(p1(FIELD)))
    print(p2(FIELD))
