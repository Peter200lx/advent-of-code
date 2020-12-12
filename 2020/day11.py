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
    locations: Dict[Coord, bool]

    @staticmethod
    def read_lines(input_str):
        lines = input_str.split("\n")
        height = len(lines)
        width = len(lines[0])
        locations: Dict[Coord, bool] = {}
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == "L":
                    locations[Coord(x, y)] = False  # All seats unoccupied
        return Map(width, height, locations)

    def next_state(self, loc: Coord, part2=False):
        loc_occupied = self.locations[loc]
        count = 0
        for direction in ADJACENT:
            next_loc = loc + direction
            next_loc_occupied = self.locations.get(next_loc, None)
            if next_loc_occupied:
                count += 1
                if (not loc_occupied and count > 0) or (loc_occupied and count >= (5 if part2 else 4)):
                    return False
                continue
            elif not part2 or next_loc_occupied is False:
                continue
            while (0 <= next_loc.x < self.width) and (0 <= next_loc.y < self.height):
                next_loc += direction
                if next_loc not in self.locations:
                    continue
                elif self.locations[next_loc]:
                    count += 1
                    if (not loc_occupied and count > 0) or (loc_occupied and (count >= (5 if part2 else 4))):
                        return False
                break
        return True if (not loc_occupied and count == 0) else loc_occupied

    def next_board(self, part2=False):
        new_map = {loc: self.next_state(loc, part2) for loc in self.locations}
        return Map(self.width, self.height, new_map)

    def fill_seats(self):
        new_map = {loc: True for loc in self.locations}
        return Map(self.width, self.height, new_map)

    def num_occupied(self):
        return sum(self.locations.values())

    def print_map(self):
        def char(loc: Coord):
            if loc not in self.locations:
                return "."
            return "#" if self.locations[loc] else "L"

        for y in range(self.height):
            print("".join(char(Coord(x, y)) for x in range(self.width)))


def find_stable(cur_map: Map, p2=False):
    cur_map = cur_map.fill_seats()
    next_map = cur_map.next_board(p2)
    while next_map != cur_map:
        cur_map, next_map = next_map, next_map.next_board(p2)
    print(next_map.num_occupied())


if __name__ == "__main__":
    DATA = (FILE_DIR / "day11.input").read_text().strip()
    start_map = Map.read_lines(DATA)
    # print(start_map)
    # start_map.print_map()
    find_stable(start_map)
    find_stable(start_map, p2=True)
