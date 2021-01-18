from hashlib import md5
import heapq
from typing import NamedTuple, Optional, List, Tuple

DATA = """qljzarfv"""
OPEN_DOORS = {"b", "c", "d", "e", "f"}
DOOR_ORDER = "UDLR"
GRID_SIZE = 4


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other) -> Optional["Coord"]:
        x, y = other.x + self.x, other.y + self.y
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
            return Coord(other.x + self.x, other.y + self.y)
        return None


DIRECTION_COORDS = {
    "U": Coord(0, -1),
    "D": Coord(0, 1),
    "L": Coord(-1, 0),
    "R": Coord(1, 0),
}
FINAL_LOC = Coord(GRID_SIZE - 1, GRID_SIZE - 1)


def available_routes(hash_so_far, loc: Coord):
    next_paths: List[Tuple[str, Coord]] = []
    next_hash = md5(hash_so_far.encode()).hexdigest()
    for i, c in enumerate(next_hash[:4]):
        if c not in OPEN_DOORS:
            continue
        direction = DOOR_ORDER[i]
        new_loc = loc + DIRECTION_COORDS[direction]
        if new_loc is None:
            continue
        next_paths.append((hash_so_far + direction, new_loc))
    return next_paths


def find_shortest_route(start_hash):
    heap: List[Tuple[int, str, Coord]] = [(len(start_hash), start_hash, Coord(0, 0))]
    last_valid = None
    while heap:
        _len, hash_so_far, loc = heapq.heappop(heap)
        for new_hash, new_loc in available_routes(hash_so_far, loc):
            if new_loc == FINAL_LOC:
                if last_valid is None:
                    print(new_hash[len(start_hash) :])
                last_valid = new_hash[len(start_hash) :]
                continue
            heapq.heappush(heap, (len(new_hash), new_hash, new_loc))
    return last_valid


if __name__ == "__main__":
    print(len(find_shortest_route(DATA)))
