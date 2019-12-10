import math
from pathlib import Path
from typing import NamedTuple, List, Tuple, Dict, Iterator


class Vector(NamedTuple):
    y: int
    x: int

    @property
    def reduced(self) -> "Vector":
        gcd = math.gcd(self.y, self.x)
        if gcd == 0:
            return self
        return Vector(self.y // gcd, self.x // gcd)

    @property
    def angle(self) -> float:
        return (math.degrees(math.atan2(self.y, self.x)) + 90) % 360

    def __lt__(self, other: "Vector") -> bool:
        return self.angle < other.angle


class Point(NamedTuple):
    y: int
    x: int

    def slope(self, other: "Point") -> Vector:
        return Vector(other.y - self.y, other.x - self.x).reduced

    def distance(self, other: "Point") -> int:
        return abs(self.y - other.y) + abs(self.x - other.x)

    def closer(self, first: "Point", second: "Point") -> "Point":
        if self.distance(first) < self.distance(second):
            return first
        else:
            return second


def generate_asteroid_points(ast_field: List[List[int]]) -> Iterator[Point]:
    height, width = (len(ast_field), len(ast_field[0]))
    for y in range(height):
        for x in range(width):
            if ast_field[y][x] == 1:
                yield Point(y, x)


def build_in_view_set(
    ast_field: List[List[int]],
) -> Tuple[int, Point, Dict[Vector, Point]]:
    asteroids = set(generate_asteroid_points(ast_field))
    max_detected = (0, Point(0, 0), {})
    for location in asteroids:
        best_view = {}
        for other_ast in asteroids - {location}:
            slope = location.slope(other_ast)
            if slope not in best_view:
                best_view[slope] = other_ast
            else:
                best_view[slope] = location.closer(other_ast, best_view[slope])
        max_detected = max((len(best_view), location, best_view), max_detected)
    return max_detected


if __name__ == "__main__":
    DATA = Path("day10.input").read_text().strip()
    int_field = [[1 if c == "#" else 0 for c in line] for line in DATA.split("\n")]

    num_in_view, best_location, in_view = build_in_view_set(int_field)
    print(num_in_view, best_location)
    twohundredth = sorted(in_view)[199]
    print(in_view[twohundredth].x * 100 + in_view[twohundredth].y)
