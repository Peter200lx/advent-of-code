import heapq
from functools import cache
from pathlib import Path
from typing import NamedTuple, Optional as Opt

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)


DIRS = {
    "^": Coord(0, -1),
    "v": Coord(0, 1),
    "<": Coord(-1, 0),
    ">": Coord(1, 0),
}

# fmt: off
NUMERIC = {
    Coord(0, 0): "7", Coord(1, 0): "8", Coord(2, 0): "9",
    Coord(0, 1): "4", Coord(1, 1): "5", Coord(2, 1): "6",
    Coord(0, 2): "1", Coord(1, 2): "2", Coord(2, 2): "3",
                      Coord(1, 3): "0", Coord(2, 3): "A",
}
DIRECT = {
                      Coord(1, 0): "^", Coord(2, 0): "A",
    Coord(0, 1): "<", Coord(1, 1): "v", Coord(2, 1): ">",
}
# fmt: on
CACHED_NUMERIC = {
    True: {
        "valid_locs": frozenset(NUMERIC.keys()),
        "key_to_loc": {s: c for c, s in NUMERIC.items()},
    },
    False: {
        "valid_locs": frozenset(DIRECT.keys()),
        "key_to_loc": {s: c for c, s in DIRECT.items()},
    },
}


@cache
def smallest_map(
    valid_locs: frozenset[Coord], from_loc: Coord, to_loc: Coord
) -> list[str]:
    to_proc = [(0, "", from_loc)]
    seen = {}
    shortest_end = 999999
    end_paths = []
    while to_proc:
        cost, path, loc = heapq.heappop(to_proc)
        if seen.get(loc, 99e9) < cost:
            continue
        seen[loc] = cost
        if loc == to_loc:
            if cost < shortest_end:
                shortest_end = cost
                end_paths = [path]
            elif cost == shortest_end:
                end_paths.append(path)
            else:
                break
        for d_str, direct in DIRS.items():
            new_loc = loc + direct
            if new_loc in valid_locs:
                heapq.heappush(to_proc, (cost + 1, path + d_str, new_loc))
    return [path + "A" for path in end_paths]


@cache
def rec(code: str, depth: int, start: Opt[Coord] = None, numeric: bool = True) -> int:
    cached_pad = CACHED_NUMERIC[numeric]
    if start is None:
        start = cached_pad["key_to_loc"]["A"]
    if not code:
        return 0
    to_loc = cached_pad["key_to_loc"][code[0]]
    next_codes = smallest_map(cached_pad["valid_locs"], start, to_loc)
    code_len = (
        len(next_codes[0])
        if depth == 0
        else min(rec(next_code, depth - 1, numeric=False) for next_code in next_codes)
    )
    return code_len + rec(code[1:], depth, to_loc, numeric)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    CODES = list(DATA.split("\n"))

    print(sum(int(code[:1]) * rec(code, 2) for code in CODES))
    print(sum(int(code[:1]) * rec(code, 25) for code in CODES))
