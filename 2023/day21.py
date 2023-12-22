import heapq
from pathlib import Path
from typing import NamedTuple, Dict

INPUT_FILE = Path(__file__).with_suffix(".input")

PART_TWO_STEPS = 26501365


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)

    def __mod__(self, max: "Coord"):
        return (self.x % max.x, self.y % max.y)


DIRS = [Coord(0, -1), Coord(0, 1), Coord(1, 0), Coord(-1, 0)]


def solve_line(nums) -> int:
    deltas = [nums[i] - nums[i - 1] for i in range(1, len(nums))]
    assert len(deltas) > 1
    if all(n == 0 for n in deltas):
        return 0
    return deltas[-1] + solve_line(deltas)


class Garden:
    def __init__(self, chunk: str):
        lines = chunk.strip().split("\n")
        self.gardens = {
            Coord(x, y): c
            for y, line in enumerate(lines)
            for x, c in enumerate(line)
            if c in {".", "S"}
        }
        self.start = next(
            Coord(x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == "S"
        )
        # Relying on a mirror being in the right and bottom most column and row
        self.max = Coord(len(lines[0]), len(lines))

    def part_one(self, max_steps: int = 64) -> int:
        to_proc = [(0, self.start)]
        polarity: Dict[Coord, int] = {}
        while to_proc:
            dist, loc = heapq.heappop(to_proc)
            if loc in polarity:
                continue
            polarity[loc] = dist
            if dist > max_steps:
                break
            new_dist = dist + 1
            for direct in DIRS:
                new_loc = loc + direct
                if new_loc in self.gardens:
                    heapq.heappush(to_proc, (new_dist, new_loc))
        return sum(v % 2 == (max_steps % 2) for v in polarity.values() if v <= max_steps)

    def part_two(self) -> int:
        max_steps = 600
        to_proc = [(0, self.start)]
        polarity: Dict[Coord, int] = {}
        last_step = 0
        while to_proc:
            dist, loc = heapq.heappop(to_proc)
            if loc in polarity:
                continue
            polarity[loc] = dist
            if dist > last_step:
                last_step = dist
            if dist > max_steps:
                break
            new_dist = dist + 1
            for direct in DIRS:
                new_loc = loc + direct
                if new_loc % self.max in self.gardens:
                    heapq.heappush(to_proc, (new_dist, new_loc))
        assert self.max.x == self.max.y, "The map must be square"
        assert self.start.x == self.start.y
        assert self.max.x // 2 == self.start.x, "We must be starting in the center"
        later_items = [
            Coord(n, sum(v % 2 == (n % 2) for v in polarity.values() if v <= n))
            for n in range(200, max_steps + 1)
            if n % self.max.x == self.start.x
        ]
        one, two, three = later_items
        # Calculating 2nd order polynomial: https://math.stackexchange.com/a/680695
        a_top = one.x * (three.y - two.y) + two.x * (one.y - three.y) + three.x * (two.y - one.y)
        a_bottom = (one.x - two.x) * (one.x - three.x) * (two.x - three.x)
        a = a_top / a_bottom
        b = (two.y - one.y) / (two.x - one.x) - a * (one.x + two.x)
        c = one.y - a * (one.x**2) - b * one.x
        # print(f"{a} * x**2 + {b} * x + {c}")
        x = PART_TWO_STEPS
        return int(a * x**2 + b * x + c)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    GARDEN = Garden(DATA)

    print(GARDEN.part_one())
    print(GARDEN.part_two())
