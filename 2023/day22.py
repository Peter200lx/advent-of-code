from pathlib import Path
from typing import List, NamedTuple, Set, Tuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Coord(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y, self.z + other.z)

    @classmethod
    def from_str(cls, chunk: str):
        x, y, z = chunk.split(",")
        return cls(int(x), int(y), int(z))


DOWN = Coord(0, 0, -1)


class Slab(NamedTuple):
    one: Coord
    two: Coord
    align: int

    @classmethod
    def from_str(cls, line: str):
        front, back = line.split("~")
        one, two = Coord.from_str(front), Coord.from_str(back)
        assert sum(one[i] == two[i] for i in range(3)) >= 2, f"{one=} {two=}"
        if one.x != two.x:
            align = 0
            if one.x > two.x:  # Put lower number first
                one, two = two, one
        elif one.y != two.y:
            align = 1
            if one.y > two.y:
                one, two = two, one
        else:
            align = 2
            if one.z > two.z:
                one, two = two, one
        return cls(one, two, align)

    def points(self) -> Set[Coord]:
        if self.align == 0:
            return {Coord(n, self.one.y, self.one.z) for n in range(self.one.x, self.two.x + 1)}
        if self.align == 1:
            return {Coord(self.one.x, n, self.one.z) for n in range(self.one.y, self.two.y + 1)}
        if self.align == 2:
            return {Coord(self.one.x, self.one.y, n) for n in range(self.one.z, self.two.z + 1)}

    def bottom_points(self) -> Set[Coord]:
        if self.align == 2:
            return {Coord(self.one.x, self.one.y, self.one.z)}
        return self.points()

    def lower(self, dist: int) -> "Slab":
        return Slab(
            Coord(self.one.x, self.one.y, self.one.z - dist),
            Coord(self.two.x, self.two.y, self.two.z - dist),
            self.align,
        )


def drop_bricks(bricks: List[Slab]) -> List[Slab]:
    bricks = sorted(bricks, key=lambda x: x.one.z)
    new_bricks = []
    minx, maxx = min(c.one.x for c in bricks), max(c.two.x for c in bricks)
    miny, maxy = min(c.one.y for c in bricks), max(c.two.y for c in bricks)
    locked_points = {Coord(x, y, 0) for x in range(minx, maxx + 1) for y in range(miny, maxy + 1)}
    for brick in bricks:
        lowest = brick.bottom_points()
        assert len(lowest & locked_points) == 0, f"Brick should not be overlapping locked points"
        for i in range(9999):
            new_lowest = set()
            stopped = False
            for c in lowest:
                lowered_c = c + DOWN
                if lowered_c in locked_points:
                    stopped = True
                    break  # lowest is the lowest we can go
                new_lowest.add(lowered_c)
            if stopped:
                break
            lowest = new_lowest
        if i:
            brick = brick.lower(i)
        new_bricks.append(brick)
        locked_points.update(brick.points())
    return new_bricks


def calc_dependencies(bricks: List[Slab]) -> Tuple[int, int]:
    # Assuming bricks have already been dropped
    b_clouds = {b: b.points() for b in bricks}
    supports = {b: set() for b in bricks}
    supporting = {}
    claimed_bricks = set()
    for brick in sorted(bricks, key=lambda x: x.two.z, reverse=True):
        dependents = set()
        for c in brick.bottom_points():
            lowered_c = c + DOWN
            for b, cloud in b_clouds.items():
                if lowered_c in cloud:
                    dependents.add(b)
                    supports[b].add(brick)
                    break
        if len(dependents) == 1:
            claimed_bricks.add(next(iter(dependents)))
        supporting[brick] = dependents

    all_fall = 0
    for key_brick in claimed_bricks:
        removed = {key_brick}
        to_proc = [b for b in supports[key_brick]]
        while to_proc:
            brick = to_proc.pop(0)
            if all(b in removed for b in supporting[brick]):
                removed.add(brick)
                to_proc.extend(supports[brick])
        all_fall += len(removed) - 1

    return len(set(bricks) - claimed_bricks), all_fall


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    BRICKS = [Slab.from_str(line) for line in DATA.split("\n")]

    DROPPED_BRICKS = drop_bricks(BRICKS)
    DISINTEGRABLE, TOTAL_DROPPED_ON_REMOVAL = calc_dependencies(DROPPED_BRICKS)
    print(DISINTEGRABLE)
    print(TOTAL_DROPPED_ON_REMOVAL)
