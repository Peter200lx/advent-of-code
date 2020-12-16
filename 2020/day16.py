import re
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple, Tuple, List, Dict

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


def parse_input(lines) -> Tuple[List[Field], List[int], List[List[int]]]:
    fields, your, near = lines.split("\n\n")
    populated_fields = []
    for line in fields.split("\n"):
        if not line:
            continue
        name, nums = line.split(": ")
        range_list = []
        for section in nums.split(" or "):
            n1, n2 = section.split("-")
            range_list.append(Range(int(n1), int(n2)))
        assert len(range_list) == 2, "Always only two ranges"
        populated_fields.append(Field(name, tuple(range_list)))
    your_ticket = []
    for line in your.split("\n"):
        if "," not in line:
            continue
        your_ticket = list(map(int, RE_NUMS.findall(line)))
    near_tickets = []
    for line in near.split("\n"):
        if "," not in line:
            continue
        near_tickets.append(list(map(int, RE_NUMS.findall(line))))
    return populated_fields, your_ticket, near_tickets


def calculate_order(all_fields: List[Field], valid_nearby_lines: List[List[int]]) -> Dict[Field, int]:
    possible_positions = [all_fields.copy() for _ in range(len(valid_nearby_lines[0]))]
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

    return {field: next(iter(locs)) for field, locs in possible_dict.items()}


def run_logic(input_str: str):
    fields, your_ticket, near_tickets = parse_input(input_str)
    part_1 = 0
    valid_tickets = []
    for ticket_line in near_tickets:
        valid_line = True
        for ticket in ticket_line:
            if any(field.valid(ticket) for field in fields):
                continue
            part_1 += ticket
            valid_line = False
        if valid_line:
            valid_tickets.append(ticket_line)
    print(part_1)
    positions = calculate_order(list(fields), valid_tickets)
    part_2 = 1
    for pos in (i for p, i in positions.items() if p.name.startswith("departure ")):
        part_2 *= your_ticket[pos]
    print(part_2)


if __name__ == "__main__":
    DATA = (FILE_DIR / "day16.input").read_text().strip()
    run_logic(DATA)
