import string
from collections import deque
from pathlib import Path
from typing import NamedTuple, List, Dict, Tuple


class Point(NamedTuple):
    y: int
    x: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.y + other.y, self.x + other.x)


ADJACENT = {
    Point(-1, 0): "inverted",
    Point(1, 0): "normal",
    Point(0, 1): "normal",
    Point(0, -1): "inverted",
}


class Warp(NamedTuple):
    name: str
    down_points: List[Point]
    up_points: List[Point]


def find_warps(maze_lines: List[str]) -> Dict[str, Warp]:
    width = len(maze_lines[3])
    height = len(maze_lines)
    warps = {}
    for y, line in enumerate(maze_lines[2:-2], start=2):
        for x, c in enumerate(line[2:width], start=2):
            if c == ".":
                for m in ADJACENT:
                    if maze_lines[y + m.y][x + m.x] in string.ascii_uppercase:
                        if ADJACENT[m] == "normal":
                            name = (
                                maze_lines[y + m.y][x + m.x]
                                + maze_lines[y + 2 * m.y][x + 2 * m.x]
                            )
                        else:
                            name = (
                                maze_lines[y + 2 * m.y][x + 2 * m.x]
                                + maze_lines[y + m.y][x + m.x]
                            )
                        warp = warps.setdefault(name, Warp(name, [], []))
                        if 4 < x < (width - 2) and 4 < y < (height - 4):
                            warp.down_points.append(Point(y, x))
                        else:
                            warp.up_points.append(Point(y, x))
    return warps


JUMP_DICT = Dict[Point, Tuple[str, Point]]


def map_warps(warps: Dict[str, Warp]) -> Tuple[Point, Point, JUMP_DICT, JUMP_DICT]:
    start = None
    end = None
    jump_up = {}
    jump_down = {}
    for warp in warps.values():
        if warp.down_points:
            jump_down[warp.down_points[0]] = (warp.name, warp.up_points[0])
            jump_up[warp.up_points[0]] = (warp.name, warp.down_points[0])
        else:
            if warp.name == "AA":
                start = warp.up_points[0]
            elif warp.name == "ZZ":
                end = warp.up_points[0]
            else:
                raise NotImplementedError(
                    f"Only AA and ZZ should be single point: {warp}"
                )
    return start, end, jump_up, jump_down


def run_maze(maze: List[str], warps: Dict[str, Warp], part_1: bool = True) -> int:
    start, end, jump_up, jump_down = map_warps(warps)
    mapping_points = deque()
    mapping_points.append((start, 0, ""))
    width = len(maze[3])
    all_depths = [[[-1] * width for _ in maze]]
    all_depths[0][start[0]][start[1]] = 0
    while mapping_points:
        current, depth, path = mapping_points.popleft()
        for loc in (
            (current[0] - 1, current[1]),
            (current[0] + 1, current[1]),
            (current[0], current[1] - 1),
            (current[0], current[1] + 1),
        ):
            if maze[loc[0]][loc[1]] != ".":
                continue
            if all_depths[depth][loc[0]][loc[1]] != -1:
                continue
            if (part_1 or not depth) and loc == end:
                return all_depths[0][current[0]][current[1]] + 1
            all_depths[depth][loc[0]][loc[1]] = (
                all_depths[depth][current[0]][current[1]] + 1
            )
            if loc in jump_down:
                wname, new_loc = jump_down[loc]
                new_depth = depth if part_1 else depth + 1
                if len(all_depths) <= new_depth:
                    all_depths.append([[-1] * width for _ in maze])
                all_depths[new_depth][new_loc[0]][new_loc[1]] = (
                    all_depths[depth][current[0]][current[1]] + 2
                )
                mapping_points.append((new_loc, new_depth, path + f"v{wname}"))
            elif (part_1 or depth) and loc in jump_up:
                wname, new_loc = jump_up[loc]
                new_depth = depth if part_1 else depth - 1
                if new_depth < 0:
                    raise NotImplementedError("Can't go above level 0")
                all_depths[new_depth][new_loc[0]][new_loc[1]] = (
                    all_depths[depth][current[0]][current[1]] + 2
                )
                mapping_points.append((new_loc, new_depth, path + f"^{wname}"))
            else:
                mapping_points.append((loc, depth, path))
    raise NotImplementedError("Failed to find the maze end")


if __name__ == "__main__":
    DATA = Path("day20.input").read_text().strip("\n")
    lines = DATA.split("\n")

    all_warps = find_warps(lines)
    print(run_maze(lines, all_warps))
    print(run_maze(lines, all_warps, part_1=False))
