from pathlib import Path
from typing import NamedTuple

FILE_DIR = Path(__file__).parent


class Instruction(NamedTuple):
    type: str
    num: int


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)

    def __mul__(self, other) -> "Coord":
        if isinstance(other, int):
            return Coord(self.x * other, self.y * other)
        elif isinstance(other, Coord):
            return Coord(self.x * other.x, self.y * other.y)
        raise NotImplementedError

    def flip(self):
        return Coord(x=self.y, y=self.x)

    def manhattan_distance(self, other) -> int:
        return abs(self.x + other.x) + abs(self.y + other.y)


DIR_MAP = {
    "E": Coord(1, 0),
    "W": Coord(-1, 0),
    "N": Coord(0, 1),
    "S": Coord(0, -1),
}

ROTATION_MAP = {
    "L": ["N", "W", "S", "E"],
    "R": ["N", "E", "S", "W"],
}

ROTATION_WAYPOINT = {
    "L": [Coord(1, 1), Coord(-1, 1), Coord(-1, -1), Coord(1, -1)],
    "R": [Coord(1, 1), Coord(1, -1), Coord(-1, -1), Coord(-1, 1)],
}


WAYPOINT_START_DELTA = Coord(x=10, y=1)


class Ship:
    def __init__(self):
        self.facing = "E"
        self.location = Coord(0, 0)
        self.locations_been = [self.location]
        self.waypoint_delta = WAYPOINT_START_DELTA

    def move_p1(self, instruction: Instruction):
        if instruction.type in DIR_MAP:
            self.location += DIR_MAP[instruction.type] * instruction.num
        elif instruction.type == "F":
            self.location += DIR_MAP[self.facing] * instruction.num
        elif instruction.type in ROTATION_MAP:
            rot_index = (instruction.num // 90) % 4
            rot_seq = ROTATION_MAP[instruction.type]
            i = rot_seq.index(self.facing)
            self.facing = rot_seq[(i + rot_index) % 4]
        self.locations_been.append(self.location)

    def read_instruction(self, instruction: Instruction):
        if instruction.type in DIR_MAP:
            self.waypoint_delta += DIR_MAP[instruction.type] * instruction.num
        elif instruction.type in ROTATION_WAYPOINT:
            rot_index = (instruction.num // 90) % 4
            if rot_index in (1, 3):
                self.waypoint_delta = self.waypoint_delta.flip()
            rot_seq = ROTATION_WAYPOINT[instruction.type]
            self.waypoint_delta *= rot_seq[rot_index]
        elif instruction.type == "F":
            self.location += self.waypoint_delta * instruction.num
            self.locations_been.append(self.location)

    def man_from_start(self):
        return self.location.manhattan_distance(self.locations_been[0])


EXAMPLE_DATA = """F10
N3
F7
R90
F11"""


if __name__ == "__main__":
    DATA = (FILE_DIR / "day12.input").read_text().strip()
    INSTRUCTIONS = [Instruction(line[0], int(line[1:])) for line in DATA.split("\n")]
    ship = Ship()
    for inst in INSTRUCTIONS:
        ship.move_p1(inst)
    print(ship.man_from_start())
    ship2 = Ship()
    for inst in INSTRUCTIONS:
        ship2.read_instruction(inst)
    print(ship2.man_from_start())
