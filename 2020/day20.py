from math import prod
from pathlib import Path
from typing import List, Tuple, Set, Optional

import numpy as np

FILE_DIR = Path(__file__).parent

CAM_PRINT = {
    True: "#",
    False: ".",
}

np.set_printoptions(linewidth=500, formatter={"bool": lambda x: CAM_PRINT[x]})

MONSTER_STR = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""

DIRECTIONS = {
    "up": lambda x, rev=False: (0, slice(None, None, -1 if rev else None)),
    "down": lambda x, rev=False: (x, slice(None, None, -1 if rev else None)),
    "left": lambda x, rev=False: (slice(None, None, -1 if rev else None), 0),
    "right": lambda x, rev=False: (slice(None, None, -1 if rev else None), x),
}

REV_DIRS = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left",
}


class Camera:
    id: int
    full_pixels: np.ndarray
    last_row: int
    default_edges: List[Tuple[bool, ...]]
    edge_hashes: Set[Tuple[bool, ...]]
    edge_neighbors: List["Camera"]

    def __init__(self, inputstr: str):
        camid, *lines = inputstr.split("\n")
        self.id = int(camid[5:-1])
        lit_pixels = []
        for y, line in enumerate(lines):
            lit_pixels.append([c == "#" for c in line])
        self.full_pixels = np.array(lit_pixels, dtype=np.bool)
        leny, lenx = self.full_pixels.shape
        last = lenx - 1
        assert lenx == leny, "We should only have squares"
        self.last_row = last
        self.default_edges = [tuple(self.full_pixels[d(last)]) for d in DIRECTIONS.values()]
        self.edge_hashes = {
            *self.default_edges,
            *{tuple(self.full_pixels[d(last, rev=True)]) for d in DIRECTIONS.values()},
        }
        self.edge_neighbors = []

    def edge_dir_hash(self, direction: str):
        return tuple(self.full_pixels[DIRECTIONS[direction](self.last_row)])

    @property
    def right_cam(self) -> Optional["Camera"]:
        right_hash = self.edge_dir_hash("right")
        try:
            return next(n for n in self.edge_neighbors if right_hash in n.edge_hashes)
        except StopIteration:
            return None

    @property
    def down_cam(self) -> Optional["Camera"]:
        down_hash = self.edge_dir_hash("down")
        try:
            return next(n for n in self.edge_neighbors if down_hash in n.edge_hashes)
        except StopIteration:
            return None

    @property
    def actual_pixels(self) -> np.ndarray:
        return self.full_pixels[1 : self.last_row, 1 : self.last_row]

    def fill_out_neighbors(self, other_cameras: List["Camera"]):
        for cam in other_cameras:
            if cam.id == self.id:
                continue
            for edge in self.default_edges:
                neighbors = []
                if edge in cam.edge_hashes:
                    neighbors.append(cam)
                if neighbors:
                    assert len(neighbors) == 1, f"Only should have a single neighbor for every edge"
                    self.edge_neighbors.append(neighbors[0])

    def _rotate_90(self):
        self.full_pixels = np.rot90(self.full_pixels)

    def _flip_vertical(self):
        self.full_pixels = np.flipud(self.full_pixels)

    def _all_rotations(self):
        for _ in range(4):
            yield
            self._rotate_90()
        self._flip_vertical()
        for _ in range(4):
            yield
            self._rotate_90()

    def corner_rotate_to_be_top_left(self):
        assert len(self.edge_neighbors) == 2, "I'm only a corner if I have exactly two neighbors"
        neighbor_hashes = self.edge_neighbors[0].edge_hashes | self.edge_neighbors[1].edge_hashes
        while not (self.edge_dir_hash("right") in neighbor_hashes and self.edge_dir_hash("down") in neighbor_hashes):
            self._rotate_90()

    def rotate_me_to_match_edge(self, coming_from_dir: str, from_cam: "Camera"):
        from_edge = from_cam.edge_dir_hash(REV_DIRS[coming_from_dir])

        rotate_iterator = self._all_rotations()
        while self.edge_dir_hash(coming_from_dir) != from_edge:
            next(rotate_iterator)

    def __repr__(self):
        return f"Camera({self.id}, {[n.id for n in self.edge_neighbors]}"


def find_hashes(cameras: List[Camera]):
    for cam in cameras:
        cam.fill_out_neighbors(cameras)
    corner_cams = [cam for cam in cameras if len(cam.edge_neighbors) == 2]
    assert len(corner_cams) == 4, "Should only be 4 corners"
    return prod(cam.id for cam in corner_cams)


def build_grid(cameras: List[Camera]) -> np.ndarray:
    a_corner = next(cam for cam in cameras if len(cam.edge_neighbors) == 2)
    a_corner.corner_rotate_to_be_top_left()
    row_start = a_corner
    full_grid = None
    while True:  # Should return out once done with last row
        tile_ids = f"{row_start.id}"
        row = row_start.actual_pixels
        cur_cam = row_start
        while True:  # Should break out once we hit end-of-row
            next_cam = cur_cam.right_cam
            if not next_cam:
                break
            tile_ids += f" | {next_cam.id}"
            next_cam.rotate_me_to_match_edge("left", cur_cam)
            row = np.concatenate((row, next_cam.actual_pixels), axis=1)
            cur_cam = next_cam
        # print(tile_ids)
        if full_grid is None:
            full_grid = row
        else:
            full_grid = np.concatenate((full_grid, row), axis=0)
        down_cam = row_start.down_cam
        if not down_cam:
            return full_grid
        down_cam.rotate_me_to_match_edge("up", row_start)
        row_start = down_cam


def build_monster(blob: str) -> np.ndarray:
    lit_pixels = []
    for y, line in enumerate(blob.strip("\n").split("\n")):
        lit_pixels.append([c == "#" for c in line])
    return np.array(lit_pixels, dtype=np.bool)


def count_monsters_in_grid(grid: np.ndarray, monster: np.ndarray) -> int:
    gridy, gridx = grid.shape
    mony, monx = monster.shape
    count = 0
    for y in range(gridy - mony + 1):
        for x in range(gridx - monx + 1):
            if np.array_equal(grid[y : y + mony, x : x + monx] & monster, monster):
                count += 1
    return count


def count_monsters_in_grid_any_rotation(grid: np.ndarray, monster: np.ndarray) -> int:
    def _rotations(old_grid: np.ndarray) -> np.ndarray:
        for _ in range(4):
            yield old_grid
            old_grid = np.rot90(old_grid)
        old_grid = np.flipud(old_grid)
        for _ in range(4):
            yield old_grid
            old_grid = np.rot90(old_grid)

    for rotated_grid in _rotations(grid):
        mon_count = count_monsters_in_grid(rotated_grid, monster)
        if mon_count != 0:
            return mon_count


EXAMPLE_DATA = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""


if __name__ == "__main__":
    DATA = (FILE_DIR / "day20.input").read_text().strip()
    CAMERAS = [Camera(camera_chunk) for camera_chunk in DATA.split("\n\n")]
    print(find_hashes(CAMERAS))
    CAMERA_GRID = build_grid(CAMERAS)
    MONSTER = build_monster(MONSTER_STR)
    NUM_MONSTERS = count_monsters_in_grid_any_rotation(CAMERA_GRID, MONSTER)
    print(np.count_nonzero(CAMERA_GRID) - np.count_nonzero(MONSTER) * NUM_MONSTERS)
