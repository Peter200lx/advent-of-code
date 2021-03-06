from collections import namedtuple
from enum import Enum
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

EXAMPLE_DATA = r"""
/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """

EXAMPLE_DATA_P2 = r"""
/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/"""

Coord = namedtuple("Coord", ["x", "y"])
# Location, Direction, Last Intersection Turn
Cart = namedtuple("Cart", ["loc", "dir", "last_iturn"])


class Dir(Enum):
    NORTH = "^"
    SOUTH = "v"
    EAST = ">"
    WEST = "<"


class Turn(Enum):
    LEFT = 1
    STRAIGHT = 2
    RIGHT = 3


NEXT_LOC = {
    Dir.NORTH: Coord(0, -1),
    Dir.SOUTH: Coord(0, 1),
    Dir.WEST: Coord(-1, 0),
    Dir.EAST: Coord(1, 0),
}

NEXT_TURN = {
    Turn.RIGHT: Turn.LEFT,
    Turn.LEFT: Turn.STRAIGHT,
    Turn.STRAIGHT: Turn.RIGHT,
}

TURN_LEFT = {
    Dir.NORTH: Dir.WEST,
    Dir.WEST: Dir.SOUTH,
    Dir.SOUTH: Dir.EAST,
    Dir.EAST: Dir.NORTH,
}

TURN_RIGHT = {
    Dir.NORTH: Dir.EAST,
    Dir.EAST: Dir.SOUTH,
    Dir.SOUTH: Dir.WEST,
    Dir.WEST: Dir.NORTH,
}

CORNER_TURN = {
    "\\": {
        Dir.WEST: Turn.RIGHT,
        Dir.EAST: Turn.RIGHT,
        Dir.NORTH: Turn.LEFT,
        Dir.SOUTH: Turn.LEFT,
    },
    "/": {
        Dir.WEST: Turn.LEFT,
        Dir.EAST: Turn.LEFT,
        Dir.NORTH: Turn.RIGHT,
        Dir.SOUTH: Turn.RIGHT,
    },
}


def parse_input(field_str_list):
    carts = {}
    for y, line in enumerate(field_str_list):
        line = list(line)
        for x, c in enumerate(line):
            location = Coord(x, y)
            if c in [enum.value for enum in Dir]:
                carts[location] = Cart(location, Dir(c), Turn.RIGHT)
                line[x] = "|" if c in ("v", "^") else "-"
        field_str_list[y] = line
    return field_str_list, carts


def step_field(field, carts, part_2=False):
    if part_2:
        if len(carts) == 1:
            print(f"Last cart on the road: {carts.keys()}")
            return False

    for loc in list(carts.keys()):
        if loc not in carts:
            continue
        cur_cart = carts[loc]
        del carts[loc]
        # Find new location to move into
        nx = loc.x + NEXT_LOC[cur_cart.dir].x
        ny = loc.y + NEXT_LOC[cur_cart.dir].y
        new_loc = Coord(nx, ny)
        # Deal with potential crash with other carts
        if new_loc in carts:
            del carts[new_loc]
            if part_2:
                print(f"We moved from {loc} to {new_loc} and crashed")
                continue
            else:
                print(f"Part 1 Crashed at: {new_loc}")
                return False

        # Read what to do next tick from the field
        is_intersection = False
        if field[ny][nx] == "+":
            is_intersection = True
            turn = NEXT_TURN[cur_cart.last_iturn]
        elif field[ny][nx] in ("\\", "/"):
            turn = CORNER_TURN[field[ny][nx]][cur_cart.dir]
        elif field[ny][nx] in ("|", "-"):
            turn = Turn.STRAIGHT
        else:
            raise Exception("We've gotten off the track somehow!")

        # Follow the instructions from the field
        new_last_itrun = cur_cart.last_iturn
        if is_intersection:
            new_last_itrun = turn
        new_dir = cur_cart.dir
        if turn == Turn.LEFT:
            new_dir = TURN_LEFT[cur_cart.dir]
        elif turn == Turn.RIGHT:
            new_dir = TURN_RIGHT[cur_cart.dir]
        carts[new_loc] = Cart(new_loc, new_dir, new_last_itrun)
    return True


def print_field(field, carts=None):
    if carts:
        for y, row in enumerate(field):
            print("".join(carts[(i, y)].dir.value if (i, y) in carts else c for i, c in enumerate(row)))
    else:
        for row in field:
            print("".join(row))


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text()

    racetrack, vehicles = parse_input(DATA.strip("\n").split("\n"))
    # print_field(racetrack)
    # print_field(racetrack, vehicles)
    # print(vehicles)
    while step_field(racetrack, vehicles):
        # print_field(racetrack, vehicles)
        pass
    while step_field(racetrack, vehicles, part_2=True):
        # print_field(racetrack, vehicles)
        pass
