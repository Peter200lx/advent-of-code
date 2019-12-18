import string
from collections import deque
from pathlib import Path
from typing import NamedTuple, Tuple

MAX_DEPTH = 9999


class FoundKey(NamedTuple):
    name: str
    loc: Tuple[int, int]
    dist: int


class State(NamedTuple):
    loc: Tuple[int, int]
    keys: frozenset


ADJACENT = [(-1, 0), (1, 0), (0, 1), (0, -1)]


def parse_data(maze_lines):
    start = (0, 0)
    pathways = {}
    for y, line in enumerate(maze_lines):
        for x, c in enumerate(line):
            if c != "#":
                location = (y, x)
                pathways[location] = c
                if c == "@":
                    start = location

    return pathways, start


def key_distance(pathways, start, keys_grabbed=None):
    if keys_grabbed is None:
        keys_grabbed = set()
    mapping_points = deque()
    mapping_points.append(start)
    new_keys = list()
    point_depth = {start: 0}
    while mapping_points:
        current = mapping_points.popleft()
        for loc in (
            (current[0] - 1, current[1]),
            (current[0] + 1, current[1]),
            (current[0], current[1] - 1),
            (current[0], current[1] + 1),
        ):
            if loc not in pathways:
                continue
            if loc in point_depth:
                continue
            char = pathways[loc]
            if char in string.ascii_uppercase:
                if char.lower() not in keys_grabbed:
                    continue
            point_depth[loc] = point_depth[current] + 1
            if char in string.ascii_lowercase:
                if char not in keys_grabbed:
                    new_keys.append(FoundKey(char, loc, point_depth[loc]))
            mapping_points.append(loc)
    return new_keys


def find_shortest_path(pathways, start, has_keys, already_checked):
    state = State(start, frozenset(has_keys))
    if state in already_checked:
        return already_checked[state]
    keys = key_distance(pathways, start, has_keys)
    if not keys:
        already_checked[state] = 0
        return 0
    already_checked[state] = min(
        k.dist
        + find_shortest_path(pathways, k.loc, has_keys | {k.name}, already_checked)
        for k in keys
    )
    return already_checked[state]


def split_paths(paths, start):
    p2_path = paths.copy()
    for wall in ((start[0] + m[0], start[1] + m[1]) for m in ADJACENT):
        del p2_path[wall]
    return (
        p2_path,
        tuple(
            (start[0] + m[0], start[1] + m[1])
            for m in ((1, 1), (-1, -1), (1, -1), (-1, 1))
        ),
    )


def find_shortest_path_p2(pathways, bots_pos, has_keys, already_checked):
    state = State(bots_pos, frozenset(has_keys))
    if state in already_checked:
        return already_checked[state]
    keys = {
        k: i
        for i, s in enumerate(bots_pos)
        for k in key_distance(pathways, s, has_keys)
    }
    if not keys:
        already_checked[state] = 0
        return 0
    already_checked[state] = min(
        k.dist
        + find_shortest_path_p2(
            pathways,
            tuple(k.loc if j == i else p for j, p in enumerate(bots_pos)),
            has_keys | {k.name},
            already_checked,
        )
        for k, i in keys.items()
    )
    return already_checked[state]


if __name__ == "__main__":
    DATA = Path("day18.input").read_text().strip()
    lines = DATA.split("\n")

    field, starting_point = parse_data(lines)
    print(find_shortest_path(field, starting_point, set(), {}))

    p2_field, bot_starts = split_paths(field, starting_point)
    print(find_shortest_path_p2(p2_field, bot_starts, set(), {}))
