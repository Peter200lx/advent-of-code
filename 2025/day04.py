from pathlib import Path
from typing import NamedTuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)


# fmt: off
p1_d = [Coord(-1, -1), Coord(0, -1), Coord(1, -1),
        Coord(-1, 0),                Coord(1, 0),
        Coord(-1, 1),  Coord(0, 1),  Coord(1, 1)]
# fmt: on


def p1(field: set[Coord]) -> set[Coord]:
    accessible = set()
    for coord in field:
        count = 0
        for direc in p1_d:
            new_loc = coord + direc
            if new_loc in field:
                count += 1
        if count < 4:
            accessible.add(coord)
    return accessible


def p2(field: set[Coord]) -> int:
    new_field = set(field)
    changed = True
    remove_count = 0
    while changed:
        to_remove = p1(new_field)
        remove_count += len(to_remove)
        new_new_field = new_field - to_remove
        changed = len(new_field) != len(new_new_field)
        new_field = new_new_field
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
