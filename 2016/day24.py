import heapq
from pathlib import Path
from typing import Tuple, Iterable, Set, List, Dict, Optional

INPUT_FILE = Path(__file__).with_suffix(".input")

Point = Tuple[int, int]


def parse_map(in_str: str) -> Tuple[Set[Point], Dict[int, Point]]:
    map: Set[Point] = set()
    poi: Dict[int, Point] = {}
    for y, line in enumerate(in_str.split("\n")):
        for x, c in enumerate(line):
            assert isinstance(c, str)
            if c == ".":
                map.add((x, y))
            elif c.isdigit():
                point = (x, y)
                map.add(point)
                poi[int(c)] = point
    return map, poi


def _dirs(loc: Point) -> Iterable[Point]:
    for point in ((-1, 0), (0, -1), (1, 0), (0, 1)):
        yield loc[0] + point[0], loc[1] + point[1]


def find_path(paths: Set[Point], poi: Dict[int, Point], start: int) -> Dict[int, int]:
    start_point = poi[start]
    rev_poi = {v: k for k, v in poi.items()}
    breadth_first: List[Tuple[int, Point]] = [(0, start_point)]
    visited: Set[Point] = {start_point}
    seen_poi: Dict[int, Optional[int]] = {start: None}
    while seen_poi.keys() != poi.keys():
        prio, loc = heapq.heappop(breadth_first)
        for newloc in _dirs(loc):
            if newloc not in paths or newloc in visited:
                continue
            visited.add(newloc)
            if newloc in rev_poi:
                seen_poi[rev_poi[newloc]] = prio + 1
            heapq.heappush(breadth_first, (prio + 1, newloc))
    return {k: v for k, v in seen_poi.items() if v is not None}


def rec_shortest(all_distances, key, seen_so_far, p2: bool = False) -> int:
    remaining_keys = all_distances.keys() - seen_so_far
    if not remaining_keys:
        return all_distances[key][0] if p2 else 0
    return min(all_distances[key][f] + rec_shortest(all_distances, f, seen_so_far | {f}, p2) for f in remaining_keys)


def find_fewest(paths: Set[Point], poi: Dict[int, Point], p2: bool = False) -> int:
    all_distances = {i: find_path(paths, poi, i) for i in poi}
    return rec_shortest(all_distances, 0, {0}, p2)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    MAP, POI = parse_map(DATA)
    print(find_fewest(MAP, POI))
    print(find_fewest(MAP, POI, p2=True))
