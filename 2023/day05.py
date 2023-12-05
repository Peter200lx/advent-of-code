from pathlib import Path
from typing import List, Tuple

INPUT_FILE = Path(__file__).with_suffix(".input")


class Mapping:
    def __init__(self, text_blob: str):
        about, *rest = text_blob.split("\n")
        conversion, _map = about.split()
        self.from_item, self.to_item = conversion.split("-to-")
        mappings = []
        for line in rest:
            d, s, r = (int(s) for s in line.split(maxsplit=2))
            mappings.append((range(s, s + r), range(d, d + r)))
        self.maps = sorted(mappings, key=lambda x: x[0].start)

    def __repr__(self) -> str:
        return f"Mapping({self.from_item}, {self.to_item}, {self.maps})"

    def map(self, value: int) -> int:
        for from_range, to_range in self.maps:
            if value < from_range.start:
                return value
            if value >= from_range.stop:
                continue
            return to_range[value - from_range.start]
        return value

    def map_ranges(self, ranges: List[range]) -> List[range]:
        new_ranges = []
        for cur_range in ranges:
            for from_range, to_range in self.maps:
                before = range(cur_range.start, min(cur_range.stop, from_range.start))
                overlap = range(
                    max(cur_range.start, from_range.start),
                    min(cur_range.stop, from_range.stop),
                )
                cur_range = range(max(cur_range.start, from_range.stop), cur_range.stop)
                if before:
                    new_ranges.append(before)
                if overlap:
                    to_start = to_range[overlap.start - from_range.start]
                    new_ranges.append(range(to_start, to_start + len(overlap)))
                if not cur_range:
                    break
            if cur_range:
                new_ranges.append(cur_range)
        return new_ranges


def parse_input(intext: str) -> Tuple[List[int], List[Mapping]]:
    initial, *maps = intext.split("\n\n")
    _start, rest = initial.split(": ")
    starting = [int(s) for s in rest.split()]
    all_mappings = [Mapping(line) for line in maps]
    return starting, all_mappings


def part_one(starting: List[int], mappings: List[Mapping]) -> int:
    lowest_location = 9e99
    for seed_index in starting:
        next_index = seed_index
        for mapping in mappings:
            next_index = mapping.map(next_index)
        lowest_location = min(lowest_location, next_index)
    return lowest_location


def part_two_ranges(starting: List[int], mappings: List[Mapping]) -> int:
    pairs = [starting[i : i + 2] for i in range(0, len(starting), 2)]
    ranges = [range(low, low + size) for low, size in pairs]
    for mapping in mappings:
        ranges = mapping.map_ranges(ranges)
    return min(r.start for r in ranges)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    START, MAPS = parse_input(DATA)

    print(part_one(START, MAPS))

    print(part_two_ranges(START, MAPS))
