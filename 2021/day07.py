import statistics
from pathlib import Path
from typing import List

FILE_DIR = Path(__file__).parent


def part1(sub_pos: List[int]) -> int:
    mean = statistics.median(sub_pos)
    return int(sum(abs(pos - mean) for pos in sub_pos))


def gen_from_average(mid: int):
    yield int(mid)
    for i in range(1, 99):
        yield int(mid - i)
        yield int(mid + i)


def calc_p2_cost(sub_pos: List[int], mid: int) -> int:
    p2cost = sum(sum(range(1, int(abs(pos - mid)) + 1)) for pos in sub_pos)
    return p2cost


def part2(sub_pos: List[int]) -> int:
    min_so_far = 9e9
    last_min = 9e9
    for mid in gen_from_average(int(statistics.mean(sub_pos))):
        min_so_far = min(min_so_far, calc_p2_cost(sub_pos, mid))
        if last_min == min_so_far:
            return min_so_far
        last_min = min_so_far
    return min_so_far


if __name__ == "__main__":
    DATA = (FILE_DIR / "day07.input").read_text().strip()
    POSITIONS = [int(line) for line in DATA.split(",")]
    print(part1(POSITIONS))
    print(part2(POSITIONS))
