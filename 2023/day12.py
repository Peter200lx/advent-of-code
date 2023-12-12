from functools import lru_cache
from pathlib import Path
from typing import Iterable, List, Tuple, Optional

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
    potential_range = sum(known_broken) + len(known_broken) - 1
    if index:  # Only add the non-broken spring if we're not in the first segment
        separator = (False,)
        max_index = len(unknown) - potential_range
    else:
        separator = tuple()
        max_index = len(unknown) - potential_range + 1
    working = 0
    for i in range(index, max_index):
        cur_broken, *remaining_broken = known_broken
        try_list = separator + ((False,) * (i - index)) + ((True,) * cur_broken)
        new_index = index + len(try_list)
        if not test_possible(unknown, index, try_list):
            continue
        if remaining_broken:
            working += recurse_tests(unknown, new_index, tuple(remaining_broken))
        else:
            try_list += (False,) * (len(unknown) - (index + len(try_list)))
            if test_possible(unknown, index, try_list):
                assert len(try_list) + index == len(unknown)
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

    def test_possible(self, springs: List[bool]):
        assert len(springs) <= len(self.broken)
        for i, item in enumerate(springs):
            if self.broken[i] is not None and item != self.broken[i]:
                return False
        return True

    def recurse_tests(self, cur_list: List[bool], known_broken: List[int]) -> List[List[bool]]:
        length = len(self.broken)
        potential_range = sum(known_broken) + len(known_broken) - 1
        working_lists = []
        start_index = 0 if not cur_list else len(cur_list) + 1
        for i in range(start_index, length - potential_range + 1):
            cur_broken, *remaining_broken = known_broken
            try_list = cur_list + ([False] * (i - len(cur_list))) + ([True] * cur_broken)
            # print(try_list)
            if not self.test_possible(try_list):
                continue
            if remaining_broken:
                working_lists.extend(self.recurse_tests(try_list, remaining_broken))
            else:
                try_list += [False] * (length - len(try_list))
                if self.test_possible(try_list):
                    assert len(try_list) == length
                    working_lists.append(try_list)
        return working_lists

    def possible_maps(self):
        working_answers = self.recurse_tests([], self.known_broken)
        return working_answers

    def num_optimized_possible_maps(self):
        working_answers = recurse_tests(tuple(self.broken), 0, tuple(self.known_broken))
        return working_answers


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    SPRINGS = [Spring(line) for line in DATA.split("\n")]

    print(sum(len(s.possible_maps()) for s in SPRINGS))

    for s in SPRINGS:
        s.times_five()

    print(sum(s.num_optimized_possible_maps() for s in SPRINGS))
