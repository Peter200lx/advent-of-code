import string
from collections import deque
from pathlib import Path
from typing import NamedTuple, Tuple, FrozenSet


class FoundKey(NamedTuple):
    name: str
    loc: Tuple[int, int]
    dist: int
    doors: FrozenSet[str]


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


def key_distance(pathways, start):
    mapping_points = deque()
    mapping_points.append((start, frozenset()))
    new_keys = list()
    width = len(pathways[0])
    depth_map = [[-1] * width for _ in pathways]
    depth_map[start[0]][start[1]] = 0
    while mapping_points:
        current, blocking_doors = mapping_points.popleft()
        for loc in (
            (current[0] - 1, current[1]),
            (current[0] + 1, current[1]),
            (current[0], current[1] - 1),
            (current[0], current[1] + 1),
        ):
            if pathways[loc[0]][loc[1]] == "#":
                continue
            if depth_map[loc[0]][loc[1]] != -1:
                continue
            char = pathways[loc[0]][loc[1]]
            if char in string.ascii_uppercase:
                blocking_doors = blocking_doors | {char.lower()}
            depth_map[loc[0]][loc[1]] = depth_map[current[0]][current[1]] + 1
            if char in string.ascii_lowercase:
                new_keys.append(
                    FoundKey(char, loc, depth_map[loc[0]][loc[1]], blocking_doors)
                )
            mapping_points.append((loc, blocking_doors))
    return new_keys


def build_key_paths(pathways, bots_pos):
    locs_to_keys = {loc: key_distance(pathways, loc) for loc in bots_pos}
    for loc in list(locs_to_keys):
        for key in locs_to_keys[loc]:
            if key.loc not in locs_to_keys:
                locs_to_keys[key.loc] = key_distance(pathways, key.loc)
    return locs_to_keys


def find_shortest_path(pathways, bots_pos, has_keys, cache, locs_to_keys):
    state = (bots_pos, has_keys)
    if state in cache:
        return cache[state]
    keys = {
        k: i
        for i, s in enumerate(bots_pos)
        for k in locs_to_keys[s]
        if k.doors.issubset(has_keys) and k.name not in has_keys
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
                locs_to_keys,
            )
            for k, i in keys.items()
        )
    return cache[state]


if __name__ == "__main__":
    DATA = Path("day18.input").read_text().strip()
    lines = DATA.split("\n")

    starting_point = find_start(lines)
    bot_starts = (starting_point,)
    print(
        find_shortest_path(
            lines, bot_starts, frozenset(), {}, build_key_paths(lines, bot_starts),
        )
    )

    p2_field, bot_starts = build_p2_map(lines, starting_point)
    print(
        find_shortest_path(
            p2_field, bot_starts, frozenset(), {}, build_key_paths(p2_field, bot_starts)
        )
    )
