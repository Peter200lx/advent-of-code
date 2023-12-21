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

    def part_two(self, max_steps: int = PART_TWO_STEPS) -> int:
        to_proc = [(0, self.start)]
        polarity: Dict[Coord, int] = {}
        last_step = 0
        while to_proc:
            dist, loc = heapq.heappop(to_proc)
            if loc in polarity:
                continue
            polarity[loc] = dist
            if dist > last_step:
                print(f"{last_step=}")
                last_step = dist
            if dist > max_steps:
                break
            new_dist = dist + 1
            for direct in DIRS:
                new_loc = loc + direct
                if new_loc % self.max in self.gardens:
                    heapq.heappush(to_proc, (new_dist, new_loc))
        later_items = [
            sum(v % 2 == (n % 2) for v in polarity.values() if v <= n)
            for n in range(200, max_steps + 1)
        ]
        for i, n in enumerate(later_items, start=200):
            print(f"{i},{n}")
        return sum(v % 2 == (max_steps % 2) for v in polarity.values() if v <= max_steps)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    GARDEN = Garden(DATA)

    print(GARDEN.part_one())
    print(GARDEN.part_two(2000))  # This printed out a CSV of steps, location_count
    # csv = [l.split(",") for l in Path("2023/day21.csv").read_text().split("\n")]
    # csv = [(int(l[0]), int(l[1])) for l in csv if l[0]]
    # Opened in LibreOffice Calc, graphed and saw a 2nd order polynomial had a R2=0.99999996 fit
    print(f"{PART_TWO_STEPS=} - 65 steps from edge = {PART_TWO_STEPS-65}")
    print(
        f"Take {PART_TWO_STEPS-65} and divide by 131 input size (it is a square) {(PART_TWO_STEPS-65)/131}"
    )
    # This means the final answer is on the edge of a square
    # Bpendragon points out https://en.wikipedia.org/wiki/Centered_square_number is the pattern
    # Extract all visited counts where the steps are on the edge of a square
    # csv = [l[1] for l in csv if l[0] % 131 == 65]
    # print(csv)
    # [94475, 185083, 305871, 456839, 637987, 849315, 1090823, 1362511, 1664379, 1996427, 2358655, 2751063, 3173651]
    # Asked https://www.wolframalpha.com/ to give the 2nd order polynomial of the above list
    #   (following hunch from LibreOffice)
    # That gave answer = 34047 + 45338*x + 15090*(x**2) on the above numbers
    print(f"x = {(PART_TWO_STEPS-65)/131 - 1=}")
    x = (PART_TWO_STEPS - 65) / 131 - 1
    print(f"answer = {34047 + 45338*x + 15090*(x**2)=}")
    print(int(34047 + 45338 * x + 15090 * (x**2)))
    # Will build a proper solution for the mystery box of WolframAlpha in a later commit
