from typing import NamedTuple, Dict

DATA = """
.##..
##.#.
##.##
.#..#
#.###""".strip()

EXAMPLE_DATA = """
....#
#..#.
#..##
..#..
#....""".strip()

OPEN = 0
BUG = 1


class Point(NamedTuple):
    y: int
    x: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.y + other.y, self.x + other.x)


ADJACENT = (Point(-1, 0), Point(1, 0), Point(0, 1), Point(0, -1))

ALL_LOCATIONS = [Point(y, x) for y in range(5) for x in range(5)]


def print_field(bug_locations: set):
    for y in range(5):
        print("".join("#" if (y, x) in bug_locations else "." for x in range(5)))


def parse_input(input_str: str) -> set:
    lines = input_str.split("\n")
    bug_locations = set()

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "#":
                bug_locations.add(Point(y, x))
    return bug_locations


def adjacent_values(bug_locs: set, loc: Point):
    return (1 for d in ADJACENT if loc + d in bug_locs)


def minute_passes(bug_locs: set) -> set:
    new_array = set()
    for loc in ALL_LOCATIONS:
        bug_count = sum(adjacent_values(bug_locs, loc))
        if loc in bug_locs:
            if bug_count == 1:
                new_array.add(loc)
        else:
            if bug_count in (1, 2):
                new_array.add(loc)
    return new_array


def calc_biodiversity(bug_locs: set) -> int:
    power = 0
    bio = 0
    for loc in ALL_LOCATIONS:
        if loc in bug_locs:
            bio += 2 ** power
        power += 1
    return bio


def part_1(bug_locs: set) -> int:
    previous_fields = {frozenset(bug_locs)}
    while True:
        bug_locs = minute_passes(bug_locs)
        array_hash = frozenset(bug_locs)
        if array_hash in previous_fields:
            return calc_biodiversity(bug_locs)
        else:
            previous_fields.add(array_hash)


def recursive_adjacent_values(recursive_bugs: Dict[int, set], level: int, loc: Point):
    for direction in ADJACENT:
        move = (loc.y + direction.y, loc.x + direction.x)
        if move == (2, 2):
            if level + 1 in recursive_bugs:
                interior_bugs = recursive_bugs[level + 1]
                if loc == (1, 2):
                    yield from (BUG for b in interior_bugs if b.y == 0)
                elif loc == (3, 2):
                    yield from (BUG for b in interior_bugs if b.y == 4)
                elif loc == (2, 1):
                    yield from (BUG for b in interior_bugs if b.x == 0)
                elif loc == (2, 3):
                    yield from (BUG for b in interior_bugs if b.x == 4)
        elif move[0] < 0:
            if level - 1 in recursive_bugs and (1, 2) in recursive_bugs[level - 1]:
                yield BUG
        elif move[0] >= 5:
            if level - 1 in recursive_bugs and (3, 2) in recursive_bugs[level - 1]:
                yield BUG
        elif move[1] < 0:
            if level - 1 in recursive_bugs and (2, 1) in recursive_bugs[level - 1]:
                yield BUG
        elif move[1] >= 5:
            if level - 1 in recursive_bugs and (2, 3) in recursive_bugs[level - 1]:
                yield BUG
        else:
            if level in recursive_bugs and move in recursive_bugs[level]:
                yield BUG


def minute_passes_recursive(recursive_bugs: Dict[int, set]) -> None:
    below = min(recursive_bugs) - 1
    above = max(recursive_bugs) + 1
    recursive_bugs[below] = set()
    recursive_bugs[above] = set()

    reference_bugs = {k: frozenset(v) for k, v in recursive_bugs.items()}
    for level in recursive_bugs:
        new_array = set()
        for loc in ALL_LOCATIONS:
            if loc == (2, 2):
                continue
            bug_count = sum(recursive_adjacent_values(reference_bugs, level, loc))
            if loc in reference_bugs[level]:
                if bug_count == 1:
                    new_array.add(loc)
            else:
                if bug_count in (1, 2):
                    new_array.add(loc)
        recursive_bugs[level] = new_array

    if not recursive_bugs[below]:
        del recursive_bugs[below]
    if not recursive_bugs[above]:
        del recursive_bugs[above]


def part_2(bug_locs: set, runtime=200) -> int:
    infinite_fields = {0: bug_locs}
    for i in range(runtime):
        minute_passes_recursive(infinite_fields)
    # for level in sorted(infinite_fields.keys()):
    #     print(f"Depth {level}:")
    #     print_field(infinite_fields[level])
    bug_count = 0
    for level, field in infinite_fields.items():
        bug_count += len(field)
    return bug_count


if __name__ == "__main__":
    scan_field = parse_input(DATA)

    print(part_1(scan_field))
    print(part_2(scan_field))
