from pathlib import Path
from typing import NamedTuple, Dict

FILE_DIR = Path(__file__).parent


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)


ADJACENT = [Coord(x, y) for x in range(-1, 2) for y in range(-1, 2) if (x, y) != (0, 0)]


class Map(NamedTuple):
    width: int
    height: int
    locations: Dict[Coord, str]

    @staticmethod
    def read_lines(input_str):
        lines = input_str.split("\n")
        height = len(lines)
        width = len(lines[0])
        locations: Dict[Coord, str] = {}
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                locations[Coord(x, y)] = c
        return Map(width, height, locations)

    def next_state(self, loc: Coord, part2=False):
        c_at_loc = self.locations[loc]
        if c_at_loc == ".":
            return "."
        count = 0
        for direction in ADJACENT:
            next_loc = loc + direction
            c_at_next_loc = self.locations.get(next_loc, ".")
            if c_at_next_loc == "#":
                count += 1
                if (c_at_loc == "L" and count > 0) or (c_at_loc == "#" and ((count >= 5) if part2 else (count >= 4))):
                    return "L"
                continue
            elif not part2 or c_at_next_loc == "L":
                continue
            while (0 <= next_loc.x < self.width) and (0 <= next_loc.y < self.height):
                next_loc += direction
                c_at_next_loc = self.locations.get(next_loc, ".")
                if c_at_next_loc == ".":
                    continue
                elif c_at_next_loc == "#":
                    count += 1
                    if (c_at_loc == "L" and count > 0) or (
                        c_at_loc == "#" and ((count >= 5) if part2 else (count >= 4))
                    ):
                        return "L"
                break
        return "#" if (c_at_loc == "L" and count == 0) else c_at_loc

    def next_board(self, part2=False):
        new_map = {}
        for loc in self.locations:
            new_map[loc] = self.next_state(loc, part2)
        return Map(self.width, self.height, new_map)

    def fill_seats(self):
        new_map = {}
        for loc, c in self.locations.items():
            if c == "L":
                new_map[loc] = "#"
            else:
                new_map[loc] = c
        return Map(self.width, self.height, new_map)

    def num_occupied(self):
        return sum(v == "#" for v in self.locations.values())

    def print_map(self):
        for y in range(self.height):
            print("".join(self.locations[Coord(x, y)] for x in range(self.width)))


def find_stable(cur_map: Map, p2=False):
    cur_map = cur_map.fill_seats()
    next_map = cur_map.next_board(p2)
    while next_map != cur_map:
        cur_map = next_map
        next_map = cur_map.next_board(p2)
    print(next_map.num_occupied())


if __name__ == "__main__":
    DATA = (FILE_DIR / "day11.input").read_text().strip()
    start_map = Map.read_lines(DATA)
    # print(start_map)
    # start_map.print_map()
    find_stable(start_map)
    find_stable(start_map, p2=True)
