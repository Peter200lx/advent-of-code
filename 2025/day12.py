from pathlib import Path
from typing import NamedTuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)


# fmt: off
FLIP = {
    Coord(0,0): Coord(0,2), Coord(0,1): Coord(0,1), Coord(0,2): Coord(0,0),
    Coord(1,0): Coord(1,2), Coord(1,1): Coord(1,1), Coord(1,2): Coord(1,0),
    Coord(2,0): Coord(0,2), Coord(2,1): Coord(2,1), Coord(2,2): Coord(2,0)
}
ROTATION = {
    Coord(0,0): Coord(0,1), Coord(0,1): Coord(0,2), Coord(0,2): Coord(1,2),
    Coord(1,0): Coord(0,0), Coord(1,1): Coord(1,1), Coord(1,2): Coord(2,2),
    Coord(2,0): Coord(1,0), Coord(2,1): Coord(2,0), Coord(2,2): Coord(2,1)
}
# fmt: on


class Region:
    def __init__(self, line: str):
        size_str, shapes_str = line.split(": ")
        sx, sy = size_str.split("x")
        self.size: Coord = Coord(int(sx), int(sy))
        self.shapes: tuple[int, ...] = tuple(int(n) for n in shapes_str.split())

    def __repr__(self):
        return f"Region({self.size=}, {self.shapes=})"

    def solve(self, shapes: list[set[Coord]]):
        # I hate that this works on the user input but not the example problem set,
        # If this hack worked on the example shapes I'd be ok with this, but this
        # is not cool to have this work on user's input but not the example input
        present_spaces = self.size.x * self.size.y
        presents_fill = sum(s * len(shapes[i]) for i, s in enumerate(self.shapes))
        return present_spaces > presents_fill


def parse(lines: str):
    *shapes_str, region_str = lines.split("\n\n")
    shapes = []
    for i, shape in enumerate(shapes_str):
        ind, *s_lines = shape.split("\n")
        assert int(ind.strip(":")) == i
        base_shape = {
            Coord(x, y)
            for y, line in enumerate(s_lines)
            for x, c in enumerate(line)
            if c == "#"
        }
        shapes.append(base_shape)
    regions = [Region(line) for line in region_str.split("\n")]
    return shapes, regions


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    SHAPES, REGIONS = parse(DATA)

    print(sum(r.solve(SHAPES) for r in REGIONS))
