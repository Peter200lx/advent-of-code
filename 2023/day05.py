from pathlib import Path
from typing import List

INPUT_FILE = Path(__file__).with_suffix(".input")


class Mapping:
    def __init__(self, text_blob):
        about, *rest = text_blob.split("\n")
        conversion, _map = about.split()
        self.from_item, self.to_item = conversion.split("-to-")
        mappings = []
        for line in rest:
            d, s, r = (int(s) for s in line.split(maxsplit=2))
            mappings.append((range(s, s + r), range(d, d + r)))
        self.maps = sorted(mappings, key=lambda x: x[0].start)

    def __repr__(self):
        return f"Mapping({self.from_item}, {self.to_item}, {self.maps})"

    def map(self, value: int):
        for from_range, to_range in self.maps:
            if value < from_range.start:
                return value
            if value >= from_range.stop:
                continue
            index = value - from_range.start
            try:
                return to_range[index]
            except:
                print(f"{value=} {from_range=} {to_range=} {index=}")
                raise
        return value

    def map_ranges(self, ranges: List[range]):
        new_ranges = []
        for cur_range in ranges:
            for from_range, to_range in self.maps:
                before = range(cur_range.start, min(cur_range.stop, from_range.start))
                overlap = range(
                    max(cur_range.start, from_range.start),
                    min(cur_range.stop, from_range.stop),
                )
                remaining = range(max(cur_range.start, from_range.stop), cur_range.stop)
                if before:
                    new_ranges.append(before)
                if overlap:
                    new_ranges.append(
                        range(
                            overlap.start - from_range.start + to_range.start,
                            overlap.stop - from_range.start + to_range.start,
                        )
                    )
                cur_range = remaining
                if not cur_range:
                    break
            if cur_range:
                new_ranges.append(cur_range)
        return new_ranges

    def update_from(self, other: "Mapping"):
        assert self.to_item == other.from_item
        self.to_item = other.to_item
        claimed_ranges = []
        my_maps = self.maps
        new_maps = []
        for my_from, my_to in my_maps:
            assert len(my_from) == len(my_to), f"{my_from=} {my_to=}"
            for other_from, other_to in other.maps:
                if other_from.stop <= my_to.stop:
                    continue
                if other_from.start >= my_to.start:
                    break
                if (
                    my_to.start < other_from.start
                ):  # I have some numbers before other range starts
                    assert len(my_from) == len(my_to), f"{my_from=} {my_to=}"
                    my_size = other_from.start - my_to.start
                    new_maps.append(
                        (
                            range(my_from.start, my_from.start + my_size),
                            range(my_to.start, my_to.start + my_size),
                        )
                    )
                    assert (
                        my_to.start + my_size == other_from.start
                    ), f"{my_to=} {my_to.start + my_size=} {my_size=} {other_from=}"
                    my_from = range(my_from.start + my_size, my_from.stop)
                    my_to = range(my_to.start + my_size, my_to.stop)
                    assert len(my_from) == len(my_to), f"{my_from=} {my_to=}"
                # Absorb the overlap
                claimed_ranges.append(range(other_from.start, my_to.stop))
                overlap_size = my_to.stop - other_from.start
                assert overlap_size == len(
                    my_from
                ), f"{my_from=} {len(my_from)=} {overlap_size=} {my_to=} {other_from=}"
                new_maps.append(
                    (my_from, range(other_to.start, other_to.start + overlap_size))
                )
                my_from = range(my_from.stop, my_from.stop)
                my_to = range(my_to.stop, my_to.stop)
                break
                # if my_to.stop - 1 in other_from:
                #     if my_to.start in other_from:
                #         # We're contained within other range
                #         claimed_ranges.append(my_to)
                #         start_index = my_to.start - other_from.start
                #         stop_index = my_to.stop - other_from.stop
                #         dest_range = range(other_to[start_index], other_to[stop_index])
                #         new_maps.append((my_from, dest_range))
            if my_to:
                new_maps.append((my_from, my_to))

        # Add in non-overlapped ranges from the other maps
        for other_from, other_to in other.maps:
            for overlapped_range in claimed_ranges:
                if overlapped_range.stop <= other_from.start:  # Overlap doesn't apply
                    continue
                if overlapped_range.start >= other_from.stop:  # We're past overlaps
                    break
                if other_from.start < overlapped_range.start:
                    other_size = overlapped_range.start - my_from.start
                    new_maps.append(
                        (
                            range(other_from.start, other_from.start + other_size),
                            range(other_to.start, other_to.start + other_size),
                        )
                    )
                    other_from = range(other_from.start + other_size, other_from.stop)
                    other_to = range(other_to.start + other_size, other_to.stop)
                # Remove the overlap
                overlap_size = len(overlapped_range)
                other_from = range(other_from.start + overlap_size, other_from.stop)
                other_to = range(other_to.start + overlap_size, other_to.stop)
            if other_from:
                new_maps.append((other_from, other_to))
        self.maps = sorted(new_maps, key=lambda x: x[0].start)


def parse_input(intext: str):
    initial, *maps = intext.split("\n\n")
    start, rest = initial.split(": ")
    starting = {start: [int(s) for s in rest.split()]}
    all_mappings = [Mapping(line) for line in maps]
    return starting, all_mappings


def part_one(starting, mappings):
    lowest_location = 9e99
    for seed_index in starting["seeds"]:
        next_index = seed_index
        for mapping in mappings:
            next_index = mapping.map(next_index)
        lowest_location = min(lowest_location, next_index)
    return lowest_location


def collapse_mappings(mappings):
    master_map, *remaining = mappings
    for other_map in remaining:
        master_map.update_from(other_map)
    print(master_map)
    return master_map


def part_two(starting, mappings):
    lowest_location = 9e99
    pairs = [starting["seeds"][i : i + 2] for i in range(0, len(starting["seeds"]), 2)]
    seen_index = set()
    master_map = collapse_mappings(mappings)
    for start, length in pairs:
        for seed_index in range(start, start + length):
            if seen_index in seen_index:
                continue
            lowest_location = min(lowest_location, master_map.map(seed_index))
            seen_index.add(seed_index)
    return lowest_location


def part_two_ranges(starting, mappings):
    pairs = [starting["seeds"][i : i + 2] for i in range(0, len(starting["seeds"]), 2)]
    ranges = [range(low, low + size) for low, size in pairs]
    for mapping in mappings:
        ranges = mapping.map_ranges(ranges)
    return min(r.start for r in ranges)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    START, MAPS = parse_input(DATA)

    print(part_one(START, MAPS))

    print(part_two_ranges(START, MAPS))
