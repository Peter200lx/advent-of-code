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


class Keypad:
    def __init__(self, layout: dict[Coord, str], start: str = "A"):
        self.loc_to_key = layout
        self.key_to_loc = {s: c for c, s in layout.items()}
        self.valid_locs = frozenset(layout.keys())
        self.cur = self.key_to_loc[start]

    @staticmethod
    @cache
    def smallest_map(
        valid_locs: frozenset[Coord], from_loc: Coord, to_loc: Coord
    ) -> str:
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
        # Find the best path:
        best_cost = 999999
        best_path = None
        for path in end_paths:
            cost = 0
            for i in range(1, len(path)):
                if path[i - 1] == path[i]:
                    cost += 1
                else:
                    cost += 3
            if path:
                if path[-1] in "^>":
                    cost -= 1
                if (
                    len(valid_locs) > 5
                    and to_loc in {Coord(0, 1), Coord(1, 1)}
                    and path[0] == "<"
                ):
                    cost -= 1
            if cost < best_cost:
                best_cost = cost
                best_path = path
        if len(end_paths) > 2:
            print(f"{end_paths=}, {best_path=}")
        return best_path + "A"

    def backdrive_seq(self, seq: str):
        res = ""
        for n_char in seq:
            res += self.smallest_map(self.valid_locs, self.cur, self.key_to_loc[n_char])
            self.cur = self.key_to_loc[n_char]
        return res


def part1(codes: list[str]) -> int:
    keypads = [
        Keypad(NUMERIC),
        Keypad(DIRECT),
        Keypad(DIRECT),
    ]
    ret = 0
    for code in codes:
        cur_code = code
        for keypad in keypads:
            cur_code = keypad.backdrive_seq(cur_code)
            # print(cur_code)
        print(f"{int(code[:-1])=} {len(cur_code)=} {cur_code=}")
        ret += int(code[:-1]) * len(cur_code)
    return ret


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
def solve(code: str, depth: int, start: Opt[Coord] = None, numeric: bool = True) -> int:
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
        else min(solve(next_code, depth - 1, numeric=False) for next_code in next_codes)
    )
    return code_len + solve(code[1:], depth, to_loc, numeric)


def part2(codes: list[str]) -> int:
    ret = 0
    for code in codes:
        code_num, steps = int(code[:-1]), solve(code, 25)
        print(f"{code_num=} {steps=}")
        ret += code_num * steps
    return ret


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    CODES = list(DATA.split("\n"))

    print(part1(CODES))
    print(Keypad.smallest_map.cache_info())
    print(part2(CODES))
    print(smallest_map.cache_info())
    print(solve.cache_info())
