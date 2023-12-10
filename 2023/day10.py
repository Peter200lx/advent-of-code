from pathlib import Path
from typing import NamedTuple, Set


INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y)

    def __mul__(self, num: int) -> "Coord":
        return Coord(self.x * num, self.y * num)


DIRS = {
    "|": [Coord(0, -1), Coord(0, 1)],
    "-": [Coord(-1, 0), Coord(1, 0)],
    "L": [Coord(0, -1), Coord(1, 0)],
    "J": [Coord(-1, 0), Coord(0, -1)],
    "7": [Coord(-1, 0), Coord(0, 1)],
    "F": [Coord(1, 0), Coord(0, 1)],
    ".": [],
    "S": [],
}


class LoopNode:
    def __init__(self, coord: Coord, char: str):
        self.coord = coord
        self.type = char
        self.neighbors = set()

    def set_start_type(self):
        assert self.type == "S"
        rev_dirs = {tuple(sorted(coords)): c for c, coords in DIRS.items()}
        rev_deltas = tuple(sorted(n.coord - self.coord for n in self.neighbors))
        self.type = rev_dirs[rev_deltas]

    def double_coords(self) -> Set[Coord]:
        coord = self.coord * 2
        if self.type == "|":
            return {coord, coord + Coord(0, 1)}
        elif self.type == "-":
            return {coord, coord + Coord(1, 0)}
        elif self.type == "L":
            return {coord, coord + Coord(1, 0)}
        elif self.type == "J":
            return {coord}
        elif self.type == "7":
            return {coord, coord + Coord(0, 1)}
        elif self.type == "F":
            return {coord, coord + Coord(0, 1), coord + Coord(1, 0)}


def print_stuff(loop, flood):
    all_tiles = set(loop) | set(flood)
    minx, maxx = min(c.x for c in all_tiles), max(c.x for c in all_tiles)
    miny, maxy = min(c.y for c in all_tiles), max(c.y for c in all_tiles)
    for y in range(miny, maxy + 1):
        print(
            "".join(
                "w"
                if Coord(x, y) in flood
                else loop[Coord(x, y)].type
                if Coord(x, y) in loop
                else "."
                for x in range(minx, maxx + 1)
            )
        )


def solve(instr: str):
    floor = {Coord(x, y): c for y, line in enumerate(instr.split("\n")) for x, c in enumerate(line)}
    start_loc = next(c for c, s in floor.items() if s == "S")
    start = LoopNode(start_loc, "S")
    for delta in (Coord(0, 1), Coord(0, -1), Coord(-1, 0), Coord(1, 0)):
        new_coord = start.coord + delta
        c = floor.get(new_coord)
        if not c:
            continue
        if delta * -1 in DIRS[c]:
            new_piece = LoopNode(new_coord, c)
            new_piece.neighbors.add(start)
            start.neighbors.add(new_piece)
    assert len(start.neighbors) == 2
    loop_half_length = 1
    cur_nodes = list(start.neighbors)
    loop_nodes = {n.coord: n for n in start.neighbors}
    loop_nodes[start_loc] = start
    while True:
        next_nodes = []
        for piece in cur_nodes:
            for delta in DIRS[piece.type]:
                new_coord = piece.coord + delta
                if not any(n.coord == new_coord for n in piece.neighbors):
                    if new_coord in loop_nodes:
                        new_node = loop_nodes[new_coord]
                    else:
                        new_node = LoopNode(new_coord, floor[new_coord])
                        loop_nodes[new_coord] = new_node
                    new_node.neighbors.add(piece)
                    next_nodes.append(new_node)
                    break
        assert len(next_nodes) == 2
        loop_half_length += 1
        if next_nodes[0] == next_nodes[1]:
            break
        cur_nodes = next_nodes

    # print_stuff(loop_nodes, set())

    start.set_start_type()

    doubled_loop_nodes = set()
    for node in loop_nodes.values():
        doubled_loop_nodes |= node.double_coords()

    minx, maxx = min(c.x for c in doubled_loop_nodes) - 1, max(c.x for c in doubled_loop_nodes) + 1
    miny, maxy = min(c.y for c in doubled_loop_nodes) - 1, max(c.y for c in doubled_loop_nodes) + 1
    flood_coords = {Coord(minx, miny)}
    to_proc = list(flood_coords)
    while to_proc:
        cur_loc = to_proc.pop()
        for delta in (Coord(0, 1), Coord(0, -1), Coord(-1, 0), Coord(1, 0)):
            next_loc = cur_loc + delta
            if next_loc not in doubled_loop_nodes and next_loc not in flood_coords:
                if minx <= next_loc.x <= maxx and miny <= next_loc.y <= maxy:
                    flood_coords.add(next_loc)
                    to_proc.append(next_loc)

    even_empty_count = 0
    for x in range(minx + 1, maxx, 2):
        for y in range(miny + 1, maxy, 2):
            loc = Coord(x, y)
            if loc not in flood_coords and loc not in doubled_loop_nodes:
                even_empty_count += 1

    # print_stuff(loop_nodes, flood_coords)
    return loop_half_length, even_empty_count


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    LOOP_HALF_LENGTH, ENCLOSED_COUNT = solve(DATA)

    print(LOOP_HALF_LENGTH)
    print(ENCLOSED_COUNT)
