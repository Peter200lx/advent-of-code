from pathlib import Path
from typing import Dict, NamedTuple, Tuple

INPUT_FILE = Path(__file__).with_suffix(".input")

PART_TWO = 1000000000


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)


def print_stuff(rocks: Dict[Coord, str]):
    minx, maxx = min(c.x for c in rocks), max(c.x for c in rocks)
    miny, maxy = min(c.y for c in rocks), max(c.y for c in rocks)
    for y in range(miny, maxy + 1):
        print("".join(rocks.get(Coord(x, y), ".") for x in range(minx, maxx + 1)))


class Floor:
    def __init__(self, chunk: str):
        lines = chunk.strip().split("\n")
        self.rocks = {
            Coord(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line) if c != "."
        }
        self.max = Coord(max(c.x for c in self.rocks), max(c.y for c in self.rocks))

    def roll_rock_north(self, rocks: Dict[Coord, str], loc: Coord):
        for y in range(loc.y - 1, -1, -1):
            if (loc.x, y) in rocks:
                return y + 1
        return 0

    def roll_rock_south(self, rocks: Dict[Coord, str], loc: Coord):
        for y in range(loc.y + 1, self.max.y + 1):
            if (loc.x, y) in rocks:
                return y - 1
        return self.max.y

    def roll_rock_west(self, rocks: Dict[Coord, str], loc: Coord):
        for x in range(loc.x - 1, -1, -1):
            if (x, loc.y) in rocks:
                return x + 1
        return 0

    def roll_rock_east(self, rocks: Dict[Coord, str], loc: Coord):
        for x in range(loc.x + 1, self.max.x + 1):
            if (x, loc.y) in rocks:
                return x - 1
        return self.max.x

    def roll_north(self, rocks: Dict[Coord, str]):
        for y in range(self.max.y + 1):
            to_move = {c for c, t in rocks.items() if c.y == y and t == "O"}
            for rock in to_move:
                new_y = self.roll_rock_north(rocks, rock)
                if new_y != rock.y:
                    rocks[Coord(rock.x, new_y)] = rocks.pop(rock)
        return rocks

    def roll_south(self, rocks: Dict[Coord, str]):
        for y in range(self.max.y, -1, -1):
            to_move = {c for c, t in rocks.items() if c.y == y and t == "O"}
            for rock in to_move:
                new_y = self.roll_rock_south(rocks, rock)
                if new_y != rock.y:
                    rocks[Coord(rock.x, new_y)] = rocks.pop(rock)
        return rocks

    def roll_west(self, rocks: Dict[Coord, str]):
        for x in range(self.max.x + 1):
            to_move = {c for c, t in rocks.items() if c.x == x and t == "O"}
            for rock in to_move:
                new_x = self.roll_rock_west(rocks, rock)
                if new_x != rock.x:
                    rocks[Coord(new_x, rock.y)] = rocks.pop(rock)
        return rocks

    def roll_east(self, rocks: Dict[Coord, str]):
        for x in range(self.max.x, -1, -1):
            to_move = {c for c, t in rocks.items() if c.x == x and t == "O"}
            for rock in to_move:
                new_x = self.roll_rock_east(rocks, rock)
                if new_x != rock.x:
                    rocks[Coord(new_x, rock.y)] = rocks.pop(rock)
        return rocks

    def spin_cycle(self, rocks: Dict[Coord, str]) -> Dict[Coord, str]:
        rocks = self.roll_north(rocks)
        rocks = self.roll_west(rocks)
        rocks = self.roll_south(rocks)
        return self.roll_east(rocks)

    def value(self, rocks: Dict[Coord, str]) -> int:
        value = 0
        for y in range(self.max.y + 1):
            value += (self.max.y - y + 1) * sum(t == "O" for c, t in rocks.items() if c.y == y)
        return value

    def part_one(self) -> int:
        new_rocks = self.roll_north(dict(self.rocks))
        return self.value(new_rocks)

    def keyify(self, rocks: Dict[Coord, str]) -> Tuple[Coord, ...]:
        return tuple(sorted({c for c in rocks if rocks[c] == "O"}))

    def part_two(self) -> int:
        rocks = dict(self.rocks)
        seen_patterns = []
        for i in range(PART_TWO):
            rocks = self.spin_cycle(rocks)
            key = self.keyify(rocks)
            if key in seen_patterns:
                prev = seen_patterns.index(key)
                delta = i - prev
                target = prev + (PART_TWO - prev) % delta
                pattern = seen_patterns[target - 1]
                return self.value({c: "O" for c in pattern})
            seen_patterns.append(key)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    FLOOR = Floor(DATA)

    print(FLOOR.part_one())

    print(FLOOR.part_two())
