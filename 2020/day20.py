from collections import defaultdict
from math import prod
from pathlib import Path
from typing import NamedTuple, Dict, List, Tuple


FILE_DIR = Path(__file__).parent


class Coord(NamedTuple):
    x: int
    y: int


class Camera:
    def __init__(self, inputstr: str):
        camid, *lines = inputstr.split("\n")
        self.id = int(camid[5:-1])
        lit_pixels = set()
        for y, line in enumerate(lines):
            lit_pixels |= {Coord(x, y) for x, c in enumerate(line) if c == "#"}
        minx, maxx = min(c.x for c in lit_pixels), max(c.x for c in lit_pixels)
        miny, maxy = min(c.y for c in lit_pixels), max(c.y for c in lit_pixels)
        edge_hashes = set()
        default_edges = []
        default_edges.append(tuple(Coord(i, miny) in lit_pixels for i in range(minx, maxx + 1)))
        edge_hashes.add(default_edges[-1])
        edge_hashes.add(tuple(Coord(i, miny) in lit_pixels for i in range(maxx, minx - 1, -1)))
        default_edges.append(tuple(Coord(i, maxy) in lit_pixels for i in range(minx, maxx + 1)))
        edge_hashes.add(default_edges[-1])
        edge_hashes.add(tuple(Coord(i, maxy) in lit_pixels for i in range(maxx, minx - 1, -1)))
        default_edges.append(tuple(Coord(minx, i) in lit_pixels for i in range(miny, maxy + 1)))
        edge_hashes.add(default_edges[-1])
        edge_hashes.add(tuple(Coord(minx, i) in lit_pixels for i in range(maxy, miny - 1, -1)))
        default_edges.append(tuple(Coord(maxx, i) in lit_pixels for i in range(miny, maxy + 1)))
        edge_hashes.add(default_edges[-1])
        edge_hashes.add(tuple(Coord(maxx, i) in lit_pixels for i in range(maxy, miny - 1, -1)))
        self.lit_pixels = lit_pixels
        self.default_edges = default_edges
        self.edge_neighbors: Dict[Tuple[bool, ...], List[Camera]] = defaultdict(list)
        self.edge_hashes = edge_hashes

    def print(self):
        print(f"Cam {self.id}:")
        minx, maxx = min(c.x for c in self.lit_pixels), max(c.x for c in self.lit_pixels)
        miny, maxy = min(c.y for c in self.lit_pixels), max(c.y for c in self.lit_pixels)
        print(f"{minx}<=x<={maxx}, {miny}<=y<={maxy}")
        for y in range(miny, maxy + 1):
            print("".join("#" if Coord(x, y) in self.lit_pixels else "." for x in range(minx, maxx + 1)))

    def fill_out_neighbors(self, other_cameras: List["Camera"]):
        for cam in other_cameras:
            if cam.id == self.id:
                continue
            for edge in self.default_edges:
                if edge in cam.edge_hashes:
                    self.edge_neighbors[edge].append(cam)
        for edge, neighbors in self.edge_neighbors.items():
            assert len(neighbors) == 1, f"Only should have a single neighbor for every edge"

    def __repr__(self):
        return f"Camera({self.id}, {[(edge, len(neighbors)) for edge, neighbors in self.edge_neighbors.items()]}"


def find_hashes(cameras: List[Camera]):
    for cam in cameras:
        cam.fill_out_neighbors(cameras)
    corner_cams = [cam for cam in cameras if len(cam.edge_neighbors) == 2]
    assert len(corner_cams) == 4, "Should only be 4 corners"
    return prod(cam.id for cam in corner_cams)


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
