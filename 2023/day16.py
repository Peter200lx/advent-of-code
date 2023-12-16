from pathlib import Path
from typing import NamedTuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)


class Move(NamedTuple):
    loc: Coord
    dir: Coord


P1_START = Move(Coord(-1, 0), Coord(1, 0))

CHANGES = {
    "|": {
        Coord(1, 0): [Coord(0, 1), Coord(0, -1)],
        Coord(-1, 0): [Coord(0, 1), Coord(0, -1)],
    },
    "-": {
        Coord(0, 1): [Coord(1, 0), Coord(-1, 0)],
        Coord(0, -1): [Coord(1, 0), Coord(-1, 0)],
    },
    "/": {
        Coord(1, 0): [Coord(0, -1)],
        Coord(-1, 0): [Coord(0, 1)],
        Coord(0, 1): [Coord(-1, 0)],
        Coord(0, -1): [Coord(1, 0)],
    },
    "\\": {
        Coord(1, 0): [Coord(0, 1)],
        Coord(-1, 0): [Coord(0, -1)],
        Coord(0, 1): [Coord(1, 0)],
        Coord(0, -1): [Coord(-1, 0)],
    },
}


class Tiles:
    def __init__(self, chunk: str):
        lines = chunk.strip().split("\n")
        self.mirrors = {
            Coord(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line) if c != "."
        }
        # Relying on a mirror being in the right and bottom most column and row
        self.max = Coord(len(lines[0]), len(lines))

    def part_one(self, start: Move) -> int:
        to_proc = [start]
        seen_movements = set()
        while to_proc:
            move = to_proc.pop()
            if move in seen_movements:
                continue
            seen_movements.add(move)
            new_loc = move.loc + move.dir
            new_type = self.mirrors.get(new_loc)
            if new_type is None:
                if 0 <= new_loc.x < self.max.x and 0 <= new_loc.y < self.max.y:
                    to_proc.append(Move(new_loc, move.dir))
                continue

            to_moves = CHANGES[new_type].get(move.dir)
            if not to_moves:
                to_proc.append(Move(new_loc, move.dir))
                continue
            for new_dir in to_moves:
                to_proc.append(Move(new_loc, new_dir))
        return len({m.loc for m in seen_movements}) - 1  # Discount the start

    def part_two(self) -> int:
        left_best = max(
            self.part_one(Move(Coord(x=-1, y=y), Coord(1, 0))) for y in range(self.max.y)
        )
        right_best = max(
            self.part_one(Move(Coord(x=self.max.x, y=y), Coord(-1, 0))) for y in range(self.max.y)
        )
        top_best = max(
            self.part_one(Move(Coord(x=x, y=-1), Coord(0, 1))) for x in range(self.max.x)
        )
        bottom_best = max(
            self.part_one(Move(Coord(x=x, y=self.max.y), Coord(0, -1))) for x in range(self.max.x)
        )
        return max(left_best, right_best, top_best, bottom_best)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    TILES = Tiles(DATA)

    print(TILES.part_one(P1_START))

    print(TILES.part_two())
