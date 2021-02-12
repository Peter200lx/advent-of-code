from collections import namedtuple
from typing import Dict, List, Tuple
from pathlib import Path

FILE_DIR = Path(__file__).parent

EXAMPLE_DATA = """^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"""  # 23

Coord = namedtuple("Coord", ["y", "x"])
RCost = namedtuple("RCost", ["path_to_room", "room"])


class Room:
    DIR_MAP = {
        "N": Coord(-1, 0),
        "S": Coord(1, 0),
        "E": Coord(0, 1),
        "W": Coord(0, -1),
    }

    REV_MAP = {
        "N": "S",
        "S": "N",
        "E": "W",
        "W": "E",
    }

    def __init__(self, all_rooms: Dict[Coord, "Room"], loc: Coord):
        self.all_rooms = all_rooms
        self.loc = loc
        self.dir_N = None
        self.dir_S = None
        self.dir_E = None
        self.dir_W = None

    def join_from(self, prev_room: "Room", from_dir: str):
        prev_name = "dir_" + self.REV_MAP[from_dir]
        setattr(self, prev_name, prev_room)

    def _add_dir(self, dir_c: str):
        dir_step = self.DIR_MAP[dir_c]
        return Coord(self.loc.y + dir_step.y, self.loc.x + dir_step.x)

    def next_room(self, dir_c: str):
        next_loc = self._add_dir(dir_c)
        if next_loc not in self.all_rooms:
            next_room = Room(self.all_rooms, next_loc)
            self.all_rooms[next_loc] = next_room
        else:
            next_room = self.all_rooms[next_loc]
        next_name = "dir_" + dir_c
        setattr(self, next_name, next_room)
        next_room.join_from(self, dir_c)
        return getattr(self, next_name)

    def next_rooms(self) -> List[Tuple[str, "Room"]]:
        return [(n[-1], getattr(self, n)) for n in self.__dir__() if n.startswith("dir_") and getattr(self, n)]

    def __eq__(self, other: "Room"):
        return self.loc == other.loc

    def __hash__(self):
        return self.loc.__hash__()

    def __repr__(self):
        def p_room(name):
            return f"{name}:" + ("|" if getattr(self, "dir_" + name) else "#")

        return f"Room({self.loc} " + ", ".join(p_room(s) for s in ["N", "S", "E", "W"]) + ")"


def parse_input(regex_string: str) -> Room:
    assert regex_string[0] == "^"
    start_room = Room({}, Coord(0, 0))
    current_room = start_room
    path_stack = []
    for c in regex_string[1:]:
        if c == "$":
            # print("Done!")
            pass
        elif c == "(":
            path_stack.append(current_room)
        elif c == "|":
            current_room = path_stack[-1]
        elif c == ")":
            current_room = path_stack.pop()
        else:
            current_room = current_room.next_room(c)
    return start_room


def distance_cost2(start_room: Room):
    seen_rooms = {}
    cur_rooms = [RCost("", start_room)]
    while cur_rooms:
        next_rooms = []
        for path_to_room, cur_room in cur_rooms:
            seen_rooms[cur_room] = path_to_room
            for next_dir, next_room in cur_room.next_rooms():
                next_rooms.append(RCost(path_to_room + next_dir, next_room))
        cur_rooms = [t for t in next_rooms if t.room not in seen_rooms]
    return seen_rooms


if __name__ == "__main__":
    DATA = (FILE_DIR / "day20.input").read_text().strip()
    starting_room = parse_input(DATA)
    paths_to_rooms = distance_cost2(starting_room)
    print(max([len(s) for s in paths_to_rooms.values()]))
    print(sum([len(s) >= 1000 for s in paths_to_rooms.values()]))
