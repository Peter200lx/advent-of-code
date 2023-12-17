import heapq
from pathlib import Path
from typing import NamedTuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)


ROTATIONS = {
    Coord(0, 1): [Coord(-1, 0), Coord(1, 0)],
    Coord(0, -1): [Coord(-1, 0), Coord(1, 0)],
    Coord(1, 0): [Coord(0, -1), Coord(0, 1)],
    Coord(-1, 0): [Coord(0, -1), Coord(0, 1)],
}


class Move(NamedTuple):
    heat: int
    loc: Coord
    dir: Coord
    dur: int  # reset when direction changes


P1_START = [Move(0, Coord(0, 0), Coord(1, 0), 0), Move(0, Coord(0, 0), Coord(0, 1), 0)]


class Blocks:
    def __init__(self, chunk: str):
        lines = chunk.strip().split("\n")
        self.blocks = {
            Coord(x, y): int(c) for y, line in enumerate(lines) for x, c in enumerate(line)
        }
        self.fact = Coord(len(lines[0]) - 1, len(lines) - 1)

    def solve(self, smallest: int = 0, largest: int = 3) -> int:
        to_proc = list(P1_START)
        heapq.heapify(to_proc)
        seen = set()

        while to_proc:
            move = heapq.heappop(to_proc)
            if (move.loc, move.dir, move.dur) in seen:
                continue
            seen.add((move.loc, move.dir, move.dur))
            new_loc = move.loc + move.dir
            new_heat = move.heat + self.blocks.get(new_loc, -1)
            if new_heat < move.heat:
                # We're off the edge, do nothing
                continue
            if new_loc == self.fact:  # We're at the factory, return heat
                if move.dur < smallest:
                    continue
                return new_heat
            if move.dur + 1 >= smallest:
                for new_dir in ROTATIONS[move.dir]:
                    heapq.heappush(to_proc, Move(new_heat, new_loc, new_dir, 0))
            if move.dur + 1 < largest:
                heapq.heappush(to_proc, Move(new_heat, new_loc, move.dir, move.dur + 1))


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    BLOCKS = Blocks(DATA)

    print(BLOCKS.solve())
    print(BLOCKS.solve(4, 10))
