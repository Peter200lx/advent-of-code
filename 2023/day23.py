from pathlib import Path
from typing import NamedTuple, Dict, Set

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


class Path:
    def __init__(self, ends, full_path):
        self.ends: Set[Coord] = ends
        self.points: Set[Coord] = full_path

    def __hash__(self):
        return hash(tuple(sorted(self.ends)))


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
        self.slopes[self.start] = "v"  # Only enter the
        self.max = Coord(len(lines[0]), len(lines))
        self.end = next(Coord(x, self.max.y - 1) for x, c in enumerate(lines[-1]) if c == ".")
        self.forests.add(self.end + SLOPES["v"])  # Block the point below end
        self.collapsed_maze = self.build_connections()
        self.baked_maze = self.bake_connections()

    def bake_connections(self) -> Dict[Coord, Dict[Coord, int]]:
        collapsed = self.collapsed_maze
        baked: Dict[Coord, Dict[Coord, int]] = {}
        for loc, loc_paths in collapsed.items():
            baked[loc] = {}
            for path in loc_paths:
                baked[loc][(path.ends - {loc}).pop()] = len(path.points) - 1
        return baked

    def build_connections(self) -> Dict[Coord, Set[Path]]:
        collapsed_maze: Dict[Coord, Set[Path]] = {}
        to_proc_forks = [(self.start, self.start + SLOPES["v"])]
        while to_proc_forks:
            path_start, path_next = to_proc_forks.pop(0)
            if any(path_next in p.points for p in collapsed_maze.get(path_start, [])):
                continue
            no_backsies = {path_start}
            next_locs = [path_next]
            while len(next_locs) == 1:
                p_loc = next_locs[0]
                no_backsies.add(p_loc)
                next_locs = []
                for d in SLOPES.values():
                    try_loc = p_loc + d
                    if try_loc in self.forests or try_loc in no_backsies:
                        continue
                    next_locs.append(try_loc)
            path = Path({path_start, p_loc}, no_backsies)
            sp_paths = collapsed_maze.setdefault(path_start, set())
            if path not in sp_paths:
                sp_paths.add(path)
            sp_paths = collapsed_maze.setdefault(p_loc, set())
            if path not in sp_paths:
                sp_paths.add(path)
                for new_path_start in next_locs:
                    if not any(new_path_start in p.points for p in sp_paths):
                        to_proc_forks.append((p_loc, new_path_start))

        return collapsed_maze

    def print(self, path):
        path = set(path)
        for y in range(self.max.y):
            print(
                "".join(
                    "O"
                    if (x, y) in path
                    else "#"
                    if (x, y) in self.forests
                    else self.slopes[(x, y)]
                    if (x, y) in self.slopes
                    else "."
                    for x in range(self.max.x)
                )
            )

    def part_one(self) -> int:
        to_proc = [(self.start, tuple(self.start))]
        seen_movements: Dict[Coord, int] = {self.start: 0}
        longest_path = None
        while to_proc:
            loc, to_here = to_proc.pop()
            if seen_movements.get(loc, 0) >= len(to_here):
                continue
            seen_movements[loc] = len(to_here)
            if loc in self.slopes:
                next_dirs = [SLOPES[self.slopes[loc]]]
            else:
                next_dirs = SLOPES.values()
            for direc in next_dirs:
                new_loc = loc + direc
                if new_loc in self.forests:
                    continue
                if new_loc in to_here:
                    continue
                next_path = to_here + (new_loc,)
                if new_loc.y == self.max.y - 1:
                    # self.print(next_path)
                    if longest_path is None or len(next_path) > len(longest_path):
                        longest_path = next_path
                        continue
                to_proc.append((new_loc, next_path))
        assert longest_path is not None
        return len(longest_path) - 2

    def part_two(self, cur_loc=None, cost_so_far=0, points_of_path=None):
        if cur_loc is None:
            cur_loc = self.start
            points_of_path = {cur_loc}
        if cur_loc == self.end:
            return cost_so_far
        longest_from_here = 0
        for next_loc, dist in self.baked_maze[cur_loc].items():
            if next_loc in points_of_path:
                continue
            longest_from_here = max(
                longest_from_here,
                self.part_two(next_loc, cost_so_far + dist, points_of_path | {next_loc}),
            )
        return longest_from_here


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    ISLAND = Island(DATA)

    print(ISLAND.part_one())
    print(ISLAND.part_two())
