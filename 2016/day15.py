import re
from typing import NamedTuple, List

DATA = """Disc #1 has 17 positions; at time=0, it is at position 5.
Disc #2 has 19 positions; at time=0, it is at position 8.
Disc #3 has 7 positions; at time=0, it is at position 1.
Disc #4 has 13 positions; at time=0, it is at position 7.
Disc #5 has 5 positions; at time=0, it is at position 1.
Disc #6 has 3 positions; at time=0, it is at position 0."""

EXAMPLE_DATA = """Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1."""

RE_NUMS = re.compile(r"-?\d+")


class Disk(NamedTuple):
    id: int
    num_pos: int
    start_pos: int


def parse_input(text: str):
    initial_disks = []
    for line in text.split("\n"):
        d_id, num_pos, _, start_pos = map(int, RE_NUMS.findall(line))
        initial_disks.append(Disk(d_id, num_pos, start_pos))
    return initial_disks


def generate_available_times(disk: Disk):
    zero_time = (disk.num_pos - disk.id) - disk.start_pos
    if zero_time < 0:
        zero_time += disk.num_pos
    while True:
        yield zero_time
        zero_time += disk.num_pos


def generate_matching_times(disks):
    disk_sizes = sorted(disks, key=lambda x: x.num_pos)
    generators = [generate_available_times(d) for d in disk_sizes]
    lineup = [[next(g), g] for g in generators]
    while not all(t[0] == lineup[0][0] for t in lineup):
        min_item = min(lineup, key=lambda x: x[0])
        min_item[0] = next(min_item[1])
    print(lineup[0][0])


if __name__ == "__main__":
    INITIAL = tuple(parse_input(DATA))
    generate_matching_times(INITIAL)
    INITIAL_P2 = tuple((*INITIAL, Disk(len(INITIAL) + 1, num_pos=11, start_pos=0)))
    generate_matching_times(INITIAL_P2)  # > 16824
