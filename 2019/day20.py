import string
from collections import deque
from pathlib import Path
from typing import NamedTuple, List

MAX_DEPTH = 9999


class Point(NamedTuple):
    y: int
    x: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.y + other.y, self.x + other.x)


class Warp(NamedTuple):
    name: str
    points: List[Point]


ADJACENT = {
    Point(-1, 0): "inverted",
    Point(1, 0): "normal",
    Point(0, 1): "normal",
    Point(0, -1): "inverted",
}


def find_warps(maze_lines):
    width = len(maze_lines[3])
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
                        if name in warps:
                            warps[name].points.append(Point(y, x))
                        else:
                            warps[name] = Warp(name, [Point(y, x)])
    return warps


def map_warps(warps):
    jumps = {}
    for warp in warps.values():
        if len(warp.points) == 2:
            jumps[warp.points[0]] = warp.points[1]
            jumps[warp.points[1]] = warp.points[0]
        else:
            if warp.name == "AA":
                start = warp.points[0]
            elif warp.name == "ZZ":
                end = warp.points[0]
            else:
                raise NotImplementedError(
                    f"Only AA and ZZ should be single point: {warp}"
                )
    return start, end, jumps


def part_1(maze, warps):
    start, end, jumps_keys = map_warps(warps)
    mapping_points = deque()
    mapping_points.append(start)
    width = len(maze[3])
    depth_map = [[MAX_DEPTH] * width for _ in maze]
    depth_map[start[0]][start[1]] = 0
    while mapping_points:
        current = mapping_points.popleft()
        if current in jumps_keys:
            new_loc = jumps_keys[current]
            del jumps_keys[current]
            del jumps_keys[new_loc]
            depth_map[new_loc[0]][new_loc[1]] = depth_map[current[0]][current[1]] + 1
            mapping_points.append(new_loc)
            continue
        for loc in (
            (current[0] - 1, current[1]),
            (current[0] + 1, current[1]),
            (current[0], current[1] - 1),
            (current[0], current[1] + 1),
        ):
            if maze[loc[0]][loc[1]] != ".":
                continue
            if depth_map[loc[0]][loc[1]] != MAX_DEPTH:
                continue
            if loc == end:
                return depth_map[current[0]][current[1]] + 1
            depth_map[loc[0]][loc[1]] = depth_map[current[0]][current[1]] + 1
            mapping_points.append(loc)
    raise NotImplementedError("Failed to find the maze end")


class WarpR(NamedTuple):
    name: str
    down_points: List[Point]
    up_points: List[Point]


def find_warps_p2(maze_lines):
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
                        if 4 < x < (width - 2) and 4 < y < (height - 4):
                            if name in warps:
                                warps[name].down_points.append(Point(y, x))
                            else:
                                warps[name] = WarpR(name, [Point(y, x)], [])
                        else:
                            if name in warps:
                                warps[name].up_points.append(Point(y, x))
                            else:
                                warps[name] = WarpR(name, [], [Point(y, x)])
    return warps


def map_warps_p2(warps):
    jump_up = {}
    jump_down = {}
    for warp in warps.values():
        if warp.down_points:
            jump_down[warp.down_points[0]] = (warp.name, warp.up_points[0])
            jump_up[warp.up_points[0]] = (warp.name, warp.down_points[0])
        else:
            if warp.name == "AA":
                start = warp.up_points[0]
                assert not warp.down_points
            elif warp.name == "ZZ":
                end = warp.up_points[0]
                assert not warp.down_points
            else:
                raise NotImplementedError(
                    f"Only AA and ZZ should be single point: {warp}"
                )
    return start, end, jump_up, jump_down


def part_2(maze, warps):
    start, end, jump_up, jump_down = map_warps_p2(warps)
    mapping_points = deque()
    mapping_points.append((start, 0, ""))
    width = len(maze[3])
    all_depths = [[[MAX_DEPTH] * width for _ in maze]]
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
            if all_depths[depth][loc[0]][loc[1]] != MAX_DEPTH:
                continue
            if not depth and loc == end:
                return all_depths[0][current[0]][current[1]] + 1
            all_depths[depth][loc[0]][loc[1]] = (
                all_depths[depth][current[0]][current[1]] + 1
            )
            if loc in jump_down:
                wname, new_loc = jump_down[loc]
                new_depth = depth + 1
                if len(all_depths) <= new_depth:
                    all_depths.append([[MAX_DEPTH] * width for _ in maze])
                all_depths[new_depth][new_loc[0]][new_loc[1]] = (
                    all_depths[depth][current[0]][current[1]] + 2
                )
                mapping_points.append((new_loc, new_depth, path + f"v{wname}"))
            elif depth and loc in jump_up:
                wname, new_loc = jump_up[loc]
                new_depth = depth - 1
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
    print(part_1(lines, all_warps))
    p2_warps = find_warps_p2(lines)
    print(part_2(lines, p2_warps))
