from math import prod
from pathlib import Path
from typing import Dict, List, Tuple, Set

import numpy as np

FILE_DIR = Path(__file__).parent

CAM_PRINT = {
    1: "#",
    0: ".",
}

np.set_printoptions(linewidth=500, formatter={"int": lambda x: CAM_PRINT[x]})


class Camera:
    id: int
    lit_pixels: np.ndarray
    default_edges: List[Tuple[int, ...]]
    edge_hashes: Set[Tuple[int, ...]]
    edge_neighbors: Dict[Tuple[int, ...], "Camera"]

    def __init__(self, inputstr: str):
        camid, *lines = inputstr.split("\n")
        self.id = int(camid[5:-1])
        lit_pixels = []
        for y, line in enumerate(lines):
            lit_pixels.append([int(c == "#") for c in line])
        self.lit_pixels = np.array(lit_pixels, dtype=np.int8)
        lenx, leny = self.lit_pixels.shape
        self.default_edges = [
            tuple(self.lit_pixels[0, :]),
            tuple(self.lit_pixels[leny - 1, :]),
            tuple(self.lit_pixels[:, 0]),
            tuple(self.lit_pixels[:, lenx - 1]),
        ]
        self.edge_hashes = {e for e in self.default_edges}
        self.edge_hashes.add(tuple(self.lit_pixels[0, ::-1]))
        self.edge_hashes.add(tuple(self.lit_pixels[leny - 1, ::-1]))
        self.edge_hashes.add(tuple(self.lit_pixels[::-1, 0]))
        self.edge_hashes.add(tuple(self.lit_pixels[::-1, lenx - 1]))
        self.edge_neighbors = {}

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
                    self.edge_neighbors[edge] = neighbors[0]

    def __repr__(self):
        return f"Camera({self.id}, {[(edge, n.id) for edge, n in self.edge_neighbors.items()]}"


def find_hashes(cameras: List[Camera]):
    for cam in cameras:
        cam.fill_out_neighbors(cameras)
    corner_cams = [cam for cam in cameras if len(cam.edge_neighbors) == 2]
    assert len(corner_cams) == 4, "Should only be 4 corners"
    return prod(cam.id for cam in corner_cams)


def build_grid(cameras: List[Camera]):
    a_corner = next(cam for cam in cameras if len(cam.edge_neighbors) == 2)
    # Assume I'm starting in the top left


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
