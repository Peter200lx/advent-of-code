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

    def next_state(self, loc: Coord):
        cur_state = self.locations[loc]
        if cur_state == ".":
            return "."
        adj_occupied = sum(self.locations.get(loc + d, ".") == "#" for d in ADJACENT)
        if cur_state == "L" and adj_occupied == 0:
            return "#"
        elif cur_state == "#" and adj_occupied >= 4:
            return "L"
        return cur_state

    def trace_line_occupied_p2(self, loc: Coord, direction: Coord):
        next_loc = loc + direction
        while (0 <= next_loc.x < self.width) and (0 <= next_loc.y < self.height):
            if self.locations[next_loc] == ".":
                next_loc += direction
                continue
            return self.locations[next_loc] == "#"
        return False

    def next_state_p2(self, loc: Coord):
        cur_state = self.locations[loc]
        if cur_state == ".":
            return "."
        adj_occupied = sum(self.trace_line_occupied_p2(loc, d) for d in ADJACENT)
        if cur_state == "L" and adj_occupied == 0:
            return "#"
        elif cur_state == "#" and adj_occupied >= 5:
            return "L"
        return cur_state

    def next_board(self, func):
        new_map = {}
        for loc in self.locations:
            new_map[loc] = func(loc)
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
    next_map = cur_map.next_board(cur_map.next_state_p2 if p2 else cur_map.next_state)
    while next_map != cur_map:
        cur_map = next_map
        next_map = cur_map.next_board(cur_map.next_state_p2 if p2 else cur_map.next_state)
    print(next_map.num_occupied())


if __name__ == "__main__":
    DATA = (FILE_DIR / "day11.input").read_text().strip()
    start_map = Map.read_lines(DATA)
    # print(start_map)
    # start_map.print_map()
    find_stable(start_map)
    find_stable(start_map, p2=True)
