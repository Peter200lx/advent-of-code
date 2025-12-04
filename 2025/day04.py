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


def p1(field: dict[Coord, set[Coord]]) -> set[Coord]:
    for loc in field:
        if not field[loc]:
            field[loc] = {new_loc for d in dirs if (new_loc := loc + d) in field}
        else:
            field[loc] = {n for n in field[loc] if n in field}
    return {c for c in field if len(field[c]) < 4}


def p2(field: dict[Coord, set[Coord]]) -> int:
    changed = True
    remove_count = 0
    while changed:
        to_remove = p1(field)
        remove_count += len(to_remove)
        new_field = {k: v for k, v in field.items() if k not in to_remove}
        changed = len(field) != len(new_field)
        field = new_field
    return remove_count


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    FIELD = {
        Coord(x, y): set()
        for y, line in enumerate(DATA.split("\n"))
        for x, c in enumerate(line)
        if c == "@"
    }

    print(len(p1(FIELD)))
    print(p2(FIELD))
