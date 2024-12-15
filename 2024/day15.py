from pathlib import Path
from typing import NamedTuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)

    def add_int(self, val):
        return Coord(self.x + val, self.y + val)


DIRS = {
    "^": Coord(0, -1),
    "v": Coord(0, 1),
    "<": Coord(-1, 0),
    ">": Coord(1, 0),
}


class Map:
    def __init__(self, data: str):
        self.map = {}
        self.bot = None
        for y, line in enumerate(data.split("\n")):
            for x, c in enumerate(line):
                if c == "@":
                    self.bot = Coord(x, y)
                elif c != ".":
                    self.map[Coord(x, y)] = c

    def p1(self, moves: str) -> int:
        for move in moves:
            new_bot = self.bot + DIRS[move]
            if new_bot not in self.map:
                self.bot = new_bot
                continue
            elif self.map[new_bot] == "#":
                continue
            elif self.map[new_bot] == "O":
                boxes = []
                cur_box = new_bot
                while self.map.get(cur_box) == "O":
                    boxes.append(cur_box)
                    cur_box += DIRS[move]
                if self.map.get(cur_box) == "#":
                    continue
                self.map[cur_box] = "O"
                del self.map[boxes[0]]
                self.bot = new_bot

        return sum(100 * p.y + p.x for p in self.map if self.map[p] == "O")


class MapWide:
    def __init__(self, data: str):
        self.map = {}
        self.bot = None
        for y, line in enumerate(data.split("\n")):
            for x, c in enumerate(line):
                if c == "@":
                    self.bot = Coord(x * 2, y)
                elif c == "#":
                    self.map[Coord(x * 2, y)] = c
                    self.map[Coord(x * 2 + 1, y)] = c
                elif c == "O":
                    self.map[Coord(x * 2, y)] = "["
                    self.map[Coord(x * 2 + 1, y)] = "]"

    def printg(self):
        minx, maxx = min(p.x for p in self.map), max(p.x for p in self.map)
        miny, maxy = min(p.y for p in self.map), max(p.y for p in self.map)
        for y in range(miny, maxy + 1):
            print(
                "".join(
                    self.map.get((x, y), "@" if (x, y) == self.bot else ".")
                    for x in range(minx, maxx + 1)
                )
            )

    def _vert_box(self, inserted_loc: Coord) -> tuple[Coord, Coord]:
        if self.map[inserted_loc] == "[":
            return inserted_loc, inserted_loc + DIRS[">"]
        elif self.map[inserted_loc] == "]":
            return inserted_loc + DIRS["<"], inserted_loc
        else:
            raise NotImplemented

    def _box_push(self, new_bot: Coord, move: str) -> bool:
        if move in "<>":
            box_parts = [new_bot]
            while self.map.get(box_parts[-1], ".") in "[]":
                box_parts.append(box_parts[-1] + DIRS[move])
            if self.map.get(box_parts[-1]) == "#":
                return False
            from_i = 0
            for i, c in enumerate(reversed(box_parts[1:])):
                to_i = len(box_parts) - 1 - i
                from_i = to_i - 1
                self.map[box_parts[to_i]] = self.map[box_parts[from_i]]
            del self.map[box_parts[from_i]]
            return True
        # Move in ^v
        levels = [{self._vert_box(new_bot)}]
        while True:
            push_list = {point + DIRS[move] for box in levels[-1] for point in box}
            next_level = set()
            for point in push_list:
                if self.map.get(point) == "#":
                    return False
                if self.map.get(point, ".") in "[]":
                    next_level.add(self._vert_box(point))
            if next_level:
                levels.append(next_level)
            else:
                break
        for level in reversed(levels):
            for box in level:
                to_box = (box[0] + DIRS[move], box[1] + DIRS[move])
                assert f"{self.map[box[0]]}{self.map[box[1]]}" == "[]"
                self.map[to_box[0]] = self.map[box[0]]
                self.map[to_box[1]] = self.map[box[1]]
                del self.map[box[0]]
                del self.map[box[1]]
        return True

    def p2(self, moves: str) -> int:
        for move in moves:
            new_bot = self.bot + DIRS[move]
            if new_bot not in self.map:
                self.bot = new_bot
                continue
            elif self.map[new_bot] == "#":
                continue
            elif self.map[new_bot] in "[]":
                if self._box_push(new_bot, move):
                    self.bot = new_bot
                continue

        return sum(100 * p.y + p.x for p in self.map if self.map[p] == "[")


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    MAP_STR, MOVES_STR = DATA.split("\n\n")
    MOVES = MOVES_STR.replace("\n", "")
    MAP = Map(MAP_STR)

    print(MAP.p1(MOVES))
    print(MapWide(MAP_STR).p2(MOVES))
