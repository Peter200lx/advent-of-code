from functools import lru_cache
from pathlib import Path
from typing import Iterable, Tuple, Optional

INPUT_FILE = Path(__file__).with_suffix(".input")

MAPPING = {"#": True, ".": False, "?": None}
REV_MAP = {True: "#", False: ".", None: "?"}


def test_possible(unknown, index: int, springs: Iterable[bool]):
    for i, item in enumerate(springs):
        if unknown[index + i] is not None and item != unknown[index + i]:
            return False
    return True


@lru_cache(maxsize=None)
def recurse_tests(
    unknown: Tuple[Optional[bool], ...], index: int, known_broken: Tuple[int, ...]
) -> int:
    max_index = len(unknown) - (sum(known_broken) + len(known_broken) - 1)
    if index:  # Only add the non-broken spring if we're not in the first segment
        separator = (False,)
    else:
        separator = tuple()
        max_index += 1
    working = 0
    for i in range(index, max_index):
        try_list = separator + ((False,) * (i - index)) + ((True,) * known_broken[0])
        if not test_possible(unknown, index, try_list):
            continue
        if len(known_broken) > 1:
            working += recurse_tests(unknown, index + len(try_list), known_broken[1:])
        else:
            to_add = len(unknown) - (index + len(try_list))
            if to_add:
                if not test_possible(unknown, index + len(try_list), (False,) * to_add):
                    continue
            working += 1
    return working


class Spring:
    def __init__(self, line: str):
        unknown, commas = line.split(maxsplit=1)
        self.broken = [MAPPING[c] for c in unknown]
        self.known_broken = [int(n) for n in commas.split(",")]
        assert len(self.known_broken) >= 2

    def __repr__(self):
        return f"Spring({''.join(REV_MAP[t] for t in self.broken)}, {self.known_broken})"

    def times_five(self):
        self.broken = ([None] + self.broken) * 5
        self.broken = self.broken[1:]  # Remove the separator from the start
        self.known_broken = self.known_broken * 5

    def possible_maps(self):
        return recurse_tests(tuple(self.broken), 0, tuple(self.known_broken))


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    SPRINGS = [Spring(line) for line in DATA.split("\n")]

    print(sum(s.possible_maps() for s in SPRINGS))

    for s in SPRINGS:
        s.times_five()

    print(sum(s.possible_maps() for s in SPRINGS))
