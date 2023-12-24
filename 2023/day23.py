from pathlib import Path
from typing import NamedTuple, Dict, Tuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)


SLOPES = {
    "^": Coord(0, -1),
    ">": Coord(1, 0),
    "v": Coord(0, 1),
    "<": Coord(-1, 0),
}


class Island:
    def __init__(self, chunk: str):
        lines = chunk.strip().split("\n")
        self.start = next(
            Coord(x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == "."
        )
        self.forests = {
            Coord(x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == "#"
        }
        self.forests.add(self.start + SLOPES["^"])  # Block the point above start
        self.slopes = {
            Coord(x, y): c
            for y, line in enumerate(lines)
            for x, c in enumerate(line)
            if c in SLOPES
        }
        self.max = Coord(len(lines[0]), len(lines))
        self.end = next(Coord(x, self.max.y - 1) for x, c in enumerate(lines[-1]) if c == ".")
        self.forests.add(self.end + SLOPES["v"])  # Block the point below end
        self.baked_maze_p1, self.baked_maze_p2 = self.bake_connections()

    def bake_connections(
        self,
    ) -> Tuple[Dict[Coord, Dict[Coord, int]], Dict[Coord, Dict[Coord, int]]]:
        baked_p1: Dict[Coord, Dict[Coord, int]] = {}
        baked_p2: Dict[Coord, Dict[Coord, int]] = {}
        to_proc_forks = [(self.start, self.start + SLOPES["v"])]
        visited_starts = set()
        while to_proc_forks:
            path_start, path_next = to_proc_forks.pop(0)
            if (path_start, path_next) in visited_starts:
                continue
            visited_starts.add((path_start, path_next))
            no_backsies = [path_start]
            next_locs = [path_next]
            while len(next_locs) == 1:
                p_loc = next_locs[0]
                no_backsies.append(p_loc)
                next_locs = []
                for d in SLOPES.values():
                    try_loc = p_loc + d
                    if try_loc in self.forests or try_loc == no_backsies[-2]:
                        continue
                    next_locs.append(try_loc)
            one_way = None
            if path_next in self.slopes:
                if path_start + SLOPES[self.slopes[path_next]] == path_next:
                    one_way = 1
                elif path_next + SLOPES[self.slopes[path_next]] == path_start:
                    one_way = -1
            prior = no_backsies[-2]
            if prior in self.slopes:
                if prior + SLOPES[self.slopes[prior]] == no_backsies[-1]:
                    assert one_way is None or one_way == 1
                    one_way = 1
                elif no_backsies[-1] + SLOPES[self.slopes[prior]] == prior:
                    assert one_way is None or one_way == -1
                    one_way = -1
            if one_way is None or one_way == 1:
                baked_p1.setdefault(path_start, {})[no_backsies[-1]] = len(no_backsies) - 1
            if one_way is None or one_way == -1:
                baked_p1.setdefault(path_start, {})[path_start] = len(no_backsies) - 1
            baked_p2.setdefault(path_start, {})[no_backsies[-1]] = len(no_backsies) - 1
            baked_p2.setdefault(no_backsies[-1], {})[path_start] = len(no_backsies) - 1
            for new_path_start in next_locs:
                to_proc_forks.append((p_loc, new_path_start))

        return baked_p1, baked_p2

    def solve(self, cur_loc=None, cost_so_far=0, points_of_path=None, p2: bool = False):
        baked = self.baked_maze_p2 if p2 else self.baked_maze_p1
        if cur_loc is None:
            cur_loc = self.start
            points_of_path = {cur_loc}
        if cur_loc == self.end:
            return cost_so_far
        longest_from_here = 0
        for next_loc, dist in baked[cur_loc].items():
            if next_loc in points_of_path:
                continue
            longest_from_here = max(
                longest_from_here,
                self.solve(next_loc, cost_so_far + dist, points_of_path | {next_loc}, p2=p2),
            )
        return longest_from_here


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    ISLAND = Island(DATA)

    print(ISLAND.solve())
    print(ISLAND.solve(p2=True))
