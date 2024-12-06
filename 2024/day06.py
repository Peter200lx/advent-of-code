from pathlib import Path
from typing import NamedTuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)


ORIENT = {
    "^": Coord(0, -1),
    ">": Coord(1, 0),
    "v": Coord(0, 1),
    "<": Coord(-1, 0),
}
ROTATE = {
    "^": ">",
    ">": "v",
    "v": "<",
    "<": "^",
}


def read(data: str) -> tuple[set[Coord], tuple[Coord, str]]:
    obs = set()
    guard = None
    for y, line in enumerate(data.split("\n")):
        for x, c in enumerate(line):
            if c == "#":
                obs.add(Coord(x, y))
            elif c in ORIENT:
                guard = Coord(x, y), c
    return obs, guard


def printg(obs, guard, been_at):
    minx, maxx = min(p.x for p in obs), max(p.x for p in obs)
    miny, maxy = min(p.y for p in obs), max(p.y for p in obs)
    for y in range(miny, maxy + 1):
        line = ""
        for x in range(minx, maxx + 1):
            if (x, y) in obs:
                line += "#"
            elif (x, y) == guard[0]:
                line += guard[1]
            elif (x, y) in been_at:
                line += "X"
            else:
                line += "."
        print(line)


def p1(obs: set[Coord], guard: tuple[Coord, str]) -> set[Coord]:
    been_at = {guard[0]}
    # printg(obs, guard, been_at)
    minx, maxx = min(p.x for p in obs), max(p.x for p in obs)
    miny, maxy = min(p.y for p in obs), max(p.y for p in obs)
    new_loc = guard[0] + ORIENT[guard[1]]
    while (minx <= new_loc.x <= maxx) and (miny <= new_loc.y <= maxy):
        if new_loc in obs:
            guard = guard[0], ROTATE[guard[1]]
        else:
            been_at.add(new_loc)
            guard = new_loc, guard[1]
        new_loc = guard[0] + ORIENT[guard[1]]
    # printg(obs, guard, been_at)
    return been_at


def p2(obs: set[Coord], guard: tuple[Coord, str], cached: set[Coord]) -> int:
    blocked_locs = obs | {guard[0]}
    cached_moves = {}
    found_locs = set()
    minx, maxx = min(p.x for p in obs), max(p.x for p in obs)
    miny, maxy = min(p.y for p in obs), max(p.y for p in obs)
    for test_loc in cached:
        if test_loc in blocked_locs:
            continue
        local_obs = obs | {test_loc}
        local_guard: tuple[Coord, str] = guard
        loop = False
        been_at = {local_guard}
        while (minx <= local_guard[0].x <= maxx) and (miny <= local_guard[0].y <= maxy):
            if local_guard in cached_moves:
                if not (
                    test_loc.x - 1 <= local_guard[0].x <= test_loc.x + 1
                    and test_loc.y - 1 <= local_guard[0].y <= test_loc.y + 1
                ):
                    new_guard = cached_moves[local_guard]
                    local_guard = new_guard
                    if local_guard in been_at:
                        loop = True
                        break
                    been_at.add(local_guard)
                    continue
            new_loc = local_guard[0] + ORIENT[local_guard[1]]
            if new_loc in local_obs:
                new_guard = local_guard[0], ROTATE[local_guard[1]]
            else:
                new_guard = new_loc, local_guard[1]
            if not (
                test_loc.x - 1 <= local_guard[0].x <= test_loc.x + 1
                and test_loc.y - 1 <= local_guard[0].y <= test_loc.y + 1
            ):
                cached_moves[local_guard] = new_guard
            local_guard = new_guard
            if local_guard in been_at:
                loop = True
                break
            been_at.add(local_guard)
        if loop:
            found_locs.add(test_loc)
    return len(found_locs)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    OBS, GUARD = read(DATA)

    STEPS = p1(OBS, GUARD)
    print(len(STEPS))
    print(p2(OBS, GUARD, STEPS))
