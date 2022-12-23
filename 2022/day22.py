import re
from pathlib import Path
from typing import List, NamedTuple, Tuple, Dict, Union

INPUT_FILE = Path(__file__).with_suffix(".input")

RE_NUMS = re.compile(r"-?\d+")


class Pos(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Pos") -> "Pos":
        return Pos(self.x + other.x, self.y + other.y)


FACING = [Pos(1, 0), Pos(0, 1), Pos(-1, 0), Pos(0, -1)]

FACE_STR = [">", "v", "<", "^"]
MAP_STR = [".", "#"]


def parse(raw_str: str) -> Tuple[Dict[Pos, int], List[Union[str, int]]]:
    map_str, inst_str = raw_str.split("\n\n")
    cloud = {}
    for y, line in enumerate(map_str.split("\n")):
        for x, c in enumerate(line):
            if c == ".":
                cloud[Pos(x, y)] = 0
            elif c == "#":
                cloud[Pos(x, y)] = 1
    inst = []
    last_turn = None if inst_str[0] in {"L", "R"} else -1
    for i, c in enumerate(inst_str):
        if c in {"L", "R"}:
            if last_turn is not None:
                inst.append(int(inst_str[last_turn + 1 : i]))
            inst.append(c)
            last_turn = i
    if last_turn is not None:
        inst.append(int(inst_str[last_turn + 1 :]))
    return cloud, inst


def find_wrap(cloud: Dict[Pos, int], point: Pos, facing: int) -> Pos:
    if facing == 0:  # right
        return Pos(min(p.x for p in cloud if p.y == point.y), point.y)
    elif facing == 1:  # down
        return Pos(point.x, min(p.y for p in cloud if p.x == point.x))
    elif facing == 2:  # left
        return Pos(max(p.x for p in cloud if p.y == point.y), point.y)
    elif facing == 3:  # up
        return Pos(point.x, max(p.y for p in cloud if p.x == point.x))


def print_path(cloud: Dict[Pos, int], path: Dict[Pos, int]):
    min_x, max_x = min(p.x for p in cloud), max(p.x for p in cloud)
    min_y, max_y = min(p.y for p in cloud), max(p.y for p in cloud)
    for y in range(min_y, max_y + 1):
        print(
            f"{y:3}  "
            + "".join(
                FACE_STR[path[Pos(x, y)]]
                if Pos(x, y) in path
                else MAP_STR[cloud[Pos(x, y)]]
                if Pos(x, y) in cloud
                else " "
                for x in range(min_x, max_x + 1)
            )
        )


def part_1(cloud: Dict[Pos, int], inst: List[Union[str, int]]) -> int:
    path = {}
    cur_point = Pos(min(p.x for p in cloud if p.y == 0), 0)
    cur_face = 0
    for todo in inst:
        if isinstance(todo, int):
            for i in range(todo):
                next_point = cur_point + FACING[cur_face]
                next_type = cloud.get(next_point)
                if next_type is None:
                    next_point = find_wrap(cloud, cur_point, cur_face)
                    next_type = cloud.get(next_point)
                if next_type == 0:
                    cur_point = next_point
                    path[cur_point] = cur_face
                    continue
                if next_type == 1:
                    break
        elif todo == "L":
            cur_face -= 1
            cur_face %= 4
        elif todo == "R":
            cur_face += 1
            cur_face %= 4
        path[cur_point] = cur_face
    # print_path(cloud, path)
    # print(cur_point, cur_face)
    return (cur_point.y + 1) * 1000 + (cur_point.x + 1) * 4 + cur_face


def find_wrap_cube(point: Pos, facing: int) -> Tuple[Pos, int]:
    if point.x in range(50, 100) and point.y < 0 and facing == 3:  #       ._.    A
        return Pos(x=0, y=point.x + 100), 0
    elif point.x in range(100, 150) and point.y < 0 and facing == 3:  #    .._    B
        return Pos(x=point.x - 100, y=200 - 1), 3
    elif point.x >= 150 and point.y in range(0, 50) and facing == 0:  #    ...| v C
        return Pos(x=100 - 1, y=(50 - point.y) + 100 - 1), 2
    elif point.x in range(100, 150) and point.y >= 50 and facing == 1:  #  .._    D
        return Pos(x=100 - 1, y=point.x - 50), 2
    elif point.x >= 100 and point.y in range(50, 100) and facing == 0:  #  .|.  v D
        return Pos(x=point.y + 50, y=50 - 1), 3
    elif point.x >= 100 and point.y in range(100, 150) and facing == 0:  # .|.  v C
        return Pos(x=150 - 1, y=(150 - 1 - point.y)), 2
    elif point.x in range(50, 100) and point.y >= 150 and facing == 1:  #  ._.    E
        return Pos(x=50 - 1, y=point.x + 100), 2
    elif point.x >= 50 and point.y in range(150, 200) and facing == 0:  #  |..  v E
        return Pos(x=point.y - 100, y=150 - 1), 3
    elif point.x in range(0, 50) and point.y >= 200 and facing == 1:  #    _..    B
        return Pos(x=point.x + 100, y=0), 1
    elif point.x < 0 and point.y in range(150, 200) and facing == 2:  #  |...  ^ A
        return Pos(x=point.y - 100, y=0), 1
    elif point.x < 0 and point.y in range(100, 150) and facing == 2:  #  |...  ^ F
        return Pos(x=50, y=150 - 1 - point.y), 0
    elif point.x in range(0, 50) and point.y < 100 and facing == 3:  #    _..    G
        return Pos(x=50, y=point.x + 50), 0
    elif point.x < 50 and point.y in range(50, 100) and facing == 2:  #   .|.  ^ G
        return Pos(x=point.y - 50, y=100), 1
    elif point.x < 50 and point.y in range(0, 50) and facing == 2:  #     .|.  ^ F
        return Pos(x=0, y=(50 - point.y) + 100 - 1), 0
    else:
        raise NotImplementedError(f"{point}, {facing}")


def test_find_wrap_cube():
    for i in range(0, 50):
        p, f = find_wrap_cube(Pos(i + 50, -1), 3)  # A
        assert f == 0
        assert find_wrap_cube(p + FACING[2], 2) == (Pos(i + 50, 0), 1)
        p, f = find_wrap_cube(Pos(i + 100, -1), 3)  # B
        assert f == 3
        assert find_wrap_cube(p + FACING[1], 1) == (Pos(i + 100, 0), 1)
        p, f = find_wrap_cube(Pos(150, i), 0)  # C
        assert f == 2
        assert find_wrap_cube(p + FACING[0], 0) == (Pos(149, i), 2)
        p, f = find_wrap_cube(Pos(i + 100, 50), 1)  # D
        assert f == 2
        assert find_wrap_cube(p + FACING[0], 0) == (Pos(i + 100, 49), 3)
        p, f = find_wrap_cube(Pos(i + 50, 150), 1)  # E
        assert f == 2
        assert find_wrap_cube(p + FACING[0], 0) == (Pos(i + 50, 149), 3)
        p, f = find_wrap_cube(Pos(-1, i + 100), 2)  # F
        assert f == 0
        assert find_wrap_cube(p + FACING[2], 2) == (Pos(0, i + 100), 0)


def part_2(cloud: Dict[Pos, int], inst: List[Union[str, int]]) -> int:
    path = {}
    cur_point = Pos(min(p.x for p in cloud if p.y == 0), 0)
    cur_face = 0
    for todo in inst:
        if isinstance(todo, int):
            for i in range(todo):
                next_point = cur_point + FACING[cur_face]
                next_face = cur_face
                next_type = cloud.get(next_point)
                if next_type is None:
                    try:
                        next_point, next_face = find_wrap_cube(next_point, next_face)
                        next_type = cloud[next_point]
                    except:
                        print_path(cloud, path)
                        print(f"{cur_point=} {cur_face=} {next_point=} {next_face=}")
                        raise
                if next_type == 0:
                    cur_point = next_point
                    cur_face = next_face
                    path[cur_point] = cur_face
                    continue
                if next_type == 1:
                    break
        elif todo == "L":
            cur_face -= 1
            cur_face %= 4
        elif todo == "R":
            cur_face += 1
            cur_face %= 4
        path[cur_point] = cur_face
    # print_path(cloud, path)
    # print(cur_point, cur_face)
    return (cur_point.y + 1) * 1000 + (cur_point.x + 1) * 4 + cur_face


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().rstrip()
    CLOUD, INSTRUCTIONS = parse(DATA)

    print(part_1(CLOUD, INSTRUCTIONS))
    print(part_2(CLOUD, INSTRUCTIONS))
