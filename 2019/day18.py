import string
from collections import deque
from pathlib import Path
from typing import NamedTuple, Tuple

MAX_DEPTH = 9999


class FoundKey(NamedTuple):
    name: str
    loc: Tuple[int, int]
    dist: int


ADJACENT = [(-1, 0), (1, 0), (0, 1), (0, -1)]


def find_start(maze_lines):
    for y, line in enumerate(maze_lines):
        for x, c in enumerate(line):
            if c == "@":
                return (y, x)


def build_p2_map(paths, start):
    p2_path = paths.copy()
    for y in (start[0] - 1, start[0], start[0] + 1):
        row = list(p2_path[y])
        if y == start[0]:
            row[start[1] - 1] = "#"
            row[start[1] + 1] = "#"
        else:
            row[start[1]] = "#"
        p2_path[y] = "".join(row)
    return (
        p2_path,
        tuple(
            (start[0] + m[0], start[1] + m[1])
            for m in ((1, 1), (-1, -1), (1, -1), (-1, 1))
        ),
    )


def key_distance(pathways, start, keys_grabbed, cache):
    state = (start, keys_grabbed)
    if state in cache:
        return cache[state]
    mapping_points = deque()
    mapping_points.append(start)
    new_keys = list()
    cache[state] = new_keys
    width = len(pathways[0])
    depth_map = [[MAX_DEPTH] * width for _ in pathways]
    depth_map[start[0]][start[1]] = 0
    while mapping_points:
        current = mapping_points.popleft()
        for loc in (
            (current[0] - 1, current[1]),
            (current[0] + 1, current[1]),
            (current[0], current[1] - 1),
            (current[0], current[1] + 1),
        ):
            if pathways[loc[0]][loc[1]] == "#":
                continue
            if depth_map[loc[0]][loc[1]] != MAX_DEPTH:
                continue
            char = pathways[loc[0]][loc[1]]
            if char in string.ascii_uppercase:
                if char.lower() not in keys_grabbed:
                    continue
            depth_map[loc[0]][loc[1]] = depth_map[current[0]][current[1]] + 1
            if char in string.ascii_lowercase:
                if char not in keys_grabbed:
                    new_keys.append(FoundKey(char, loc, depth_map[loc[0]][loc[1]]))
            mapping_points.append(loc)
    return new_keys


def find_shortest_path(pathways, bots_pos, has_keys, cache, key_cache):
    state = (bots_pos, has_keys)
    if state in cache:
        return cache[state]
    keys = {
        k: i
        for i, s in enumerate(bots_pos)
        for k in key_distance(pathways, s, has_keys, key_cache)
    }
    if not keys:
        cache[state] = 0
    else:
        cache[state] = min(
            k.dist
            + find_shortest_path(
                pathways,
                tuple(k.loc if j == i else p for j, p in enumerate(bots_pos)),
                has_keys | {k.name},
                cache,
                key_cache,
            )
            for k, i in keys.items()
        )
    return cache[state]


if __name__ == "__main__":
    DATA = Path("day18.input").read_text().strip()
    lines = DATA.split("\n")

    starting_point = find_start(lines)
    print(find_shortest_path(lines, (starting_point,), frozenset(), {}, {}))

    p2_field, bot_starts = build_p2_map(lines, starting_point)
    print(find_shortest_path(p2_field, bot_starts, frozenset(), {}, {}))
