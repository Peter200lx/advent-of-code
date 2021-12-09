from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, NamedTuple, Set

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)


ADJACENT = [
    Coord(-1, 0),
    Coord(1, 0),
    Coord(0, 1),
    Coord(0, -1),
]


@dataclass
class Square:
    coord: Coord
    num: int

    def part1(self, floor: Dict[Coord, "Square"]) -> int:
        for rel in ADJACENT:
            sq = floor.get(self.coord + rel)
            other_n = sq.num if sq else 99
            if other_n <= self.num:
                return 0
        return self.num + 1


def part2(floor: Dict[Coord, Square]) -> int:
    possible_spots = {sq.coord for sq in floor.values() if sq.num != 9}
    known_groups: List[Set[Coord]] = []
    while possible_spots:
        start = possible_spots.pop()
        known_groups.append({start})
        real = possible_spots & {start + adj for adj in ADJACENT}
        to_check = set(real)
        while to_check:
            possible_spots -= real
            known_groups[-1] |= real
            nxt = to_check.pop()
            real = possible_spots & {nxt + adj for adj in ADJACENT}
            to_check |= real
    count = 1
    for group in sorted(known_groups, key=lambda x: -len(x))[:3]:
        count *= len(group)
    return count


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    FLOOR = {
        Coord(x, y): Square(Coord(x, y), int(n))
        for y, line in enumerate(DATA.split("\n"))
        for x, n in enumerate(line)
    }
    print(sum(sq.part1(FLOOR) for sq in FLOOR.values()))
    print(part2(FLOOR))
