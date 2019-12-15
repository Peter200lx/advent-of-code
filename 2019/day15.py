from enum import Enum
from pathlib import Path
from typing import List, NamedTuple, Dict

from processor import Processor


class Point(NamedTuple):
    y: int
    x: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.y + other.y, self.x + other.x)

    def __mul__(self, other) -> "Point":
        if isinstance(other, int):
            return Point(self.y * other, self.x * other)
        else:
            raise NotImplementedError(f"Multiplication of Point and {type(other)}")


class TileID(Enum):
    WALL = 0
    EMPTY = 1
    OXYGEN = 2
    UNKNOWN = 3


class Directions(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


MOVE_VEC = {
    Point(-1, 0): Directions.NORTH,
    Point(1, 0): Directions.SOUTH,
    Point(0, 1): Directions.WEST,
    Point(0, -1): Directions.EAST,
}


def print_room(room: Dict[Point, TileID]) -> None:
    miny = min(p.y for p in room)
    maxy = max(p.y for p in room)
    minx = min(p.x for p in room)
    maxx = max(p.x for p in room)
    for row in range(miny, maxy + 1):
        line = [room.get(Point(row, x), TileID.UNKNOWN) for x in range(minx, maxx + 1)]
        try:
            print("".join("#.O?"[i.value] for i in line))
        except AttributeError:
            print(line)
            raise


def run_bot(program: List[int], debug: int = 0) -> Dict[Point, TileID]:
    location = Point(0, 0)
    room = {location: TileID.EMPTY}
    running_bot = Processor(program, debug=debug).run_on_input_generator()
    next(running_bot)  # Move to first yield for .send(
    path = []
    try:
        while True:
            if debug:
                print_room(room)
                print(location)
            nearby = [move for move in MOVE_VEC if (location + move) not in room]
            if not nearby:
                next_move = path.pop() * -1
                if not path:
                    return room
                running_bot.send(MOVE_VEC[next_move].value)
                location = location + next_move
                continue

            next_move = nearby[0]
            next_loc = location + next_move
            (status,) = running_bot.send(MOVE_VEC[next_move].value)
            room[next_loc] = TileID(status)
            if room[next_loc] != TileID.WALL:
                location = next_loc
                path.append(next_move)
            if room[next_loc] == TileID.OXYGEN:
                print(len(path))  # Part 1

    except StopIteration:
        raise NotImplementedError(f"Don't expect the bot to ever halt the program")


def fill_oxygen(room: Dict[Point, TileID]) -> int:
    oxygen_start = [loc for loc, t in room.items() if t == TileID.OXYGEN][0]
    room = {loc for loc, t in room.items() if t == TileID.EMPTY}
    minutes = 0
    spread_locations = {oxygen_start}
    while room:
        spread_locations = {
            spread_point + move
            for move in MOVE_VEC
            for spread_point in spread_locations
            if spread_point + move in room
        }
        room -= spread_locations
        minutes += 1
    return minutes


if __name__ == "__main__":
    DATA = Path("day15.input").read_text().strip()
    int_list = [int(i) for i in DATA.split(",")]

    locations = run_bot(int_list)
    print(fill_oxygen(locations))
