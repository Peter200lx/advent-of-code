import re
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple, Tuple, List

FILE_DIR = Path(__file__).parent


RE_NUMS = re.compile(r"-?\d+")


class Range(NamedTuple):
    low: int
    high: int

    def valid(self, num: int):
        return self.low <= num <= self.high


class Field(NamedTuple):
    name: str
    ranges: Tuple[Range, Range]

    def valid(self, num: int):
        return any(r.valid(num) for r in self.ranges)


def parse_input(lines):
    ranges, your, near = lines.split("\n\n")
    ranges_dict = {}
    for line in ranges.split("\n"):
        if not line:
            continue
        name, nums = line.split(": ")
        range_list = []
        for rang in nums.split(" or "):
            r1, r2 = rang.split("-")
            range_list.append(Range(int(r1), int(r2)))
        assert len(range_list) == 2, "Always only two ranges"
        ranges_dict[name] = Field(name, tuple(range_list))
    your_tickets = []
    for line in your.split("\n"):
        if "," not in line:
            continue
        your_tickets = list(map(int, RE_NUMS.findall(line)))
    near_tickets = []
    for line in near.split("\n"):
        if "," not in line:
            continue
        near_tickets.append(list(map(int, RE_NUMS.findall(line))))
    return ranges_dict, your_tickets, near_tickets


def calculate_order(all_fields: List[Field], valid_nearby_lines: List[List[int]]):
    possible_positions = [list(all_fields) for _ in range(len(valid_nearby_lines[0]))]
    for ticket_line in valid_nearby_lines:
        for i, number in enumerate(ticket_line):
            still_possible = [f for f in possible_positions[i] if f.valid(number)]
            assert still_possible, "If nothing is possible we have already failed"
            possible_positions[i] = still_possible

    possible_dict = defaultdict(set)
    for i, fields in enumerate(possible_positions):
        for field in fields:
            possible_dict[field].add(i)

    for field, possible in sorted(possible_dict.items(), key=lambda x: len(x[1])):
        if len(possible) == 1:
            to_remove_i = next(iter(possible))
            for key in possible_dict:
                if key == field:
                    continue
                if to_remove_i in possible_dict[key]:
                    possible_dict[key].discard(to_remove_i)

    return possible_dict


if __name__ == "__main__":
    DATA = (FILE_DIR / "day16.input").read_text().strip()
    r, y, n = parse_input(DATA)
    total = 0
    valid = []
    for ticket_line in n:
        valid_line = True
        for ticket in ticket_line:
            if any(rang.valid(ticket) for rang in r.values()):
                continue
            total += ticket
            valid_line = False
        if valid_line:
            valid.append(ticket_line)
    print(total)
    positions = calculate_order(list(r.values()), valid)
    part_2 = 1
    for pos in (next(iter(i)) for p, i in positions.items() if p.name.startswith("departure ")):
        part_2 *= y[pos]
    print(part_2)
