from pathlib import Path
from typing import NamedTuple, Tuple, List, Set

INPUT_FILE = Path(__file__).with_suffix(".input")


# fmt: off
directions = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]
# fmt: on


class Part(NamedTuple):
    symbol: str
    loc: Tuple[int, int]
    nums: Set[Tuple[Tuple[int, int], int]]

    def is_gear(self):
        return self.symbol == "*" and len(self.nums) == 2

    def ratio(self):
        nums = list(self.nums)
        return nums[0][1] * nums[1][1]


def parse_input(raw: str) -> List[Part]:
    parts = []
    all_lines = raw.split("\n")
    for y, line in enumerate(all_lines):
        for x, c in enumerate(line):
            if not (c.isdigit() or c == "."):
                nums = set()
                for dy, dx in directions:
                    newy, newx = y + dy, x + dx
                    if not (0 <= newy < len(all_lines) and 0 <= newx <= len(line)):
                        continue
                    digit = all_lines[newy][newx]
                    if digit.isdigit():
                        dig_start = dig_end = newx
                        while dig_start >= 0 and all_lines[newy][dig_start].isdigit():
                            dig_start -= 1
                        while (
                            dig_end < len(all_lines[newy])
                            and all_lines[newy][dig_end].isdigit()
                        ):
                            dig_end += 1
                        loc = (newy, dig_start + 1)
                        nums.add((loc, int(all_lines[newy][dig_start + 1 : dig_end])))
                parts.append(Part(c, (y, x), nums))
    return parts


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    PARTS = parse_input(DATA)

    print(sum(n for part in PARTS for _loc, n in part.nums))

    print(sum(g.ratio() for g in PARTS if g.is_gear()))
