from pathlib import Path
from typing import List, Tuple, Optional

INPUT_FILE = Path(__file__).with_suffix(".input")

LARGEST_SIZE = 100000
DISK_SIZE = 70000000
PATCH_SIZE = 30000000


class Dir:
    def __init__(self, name: str, parent: Optional["Dir"] = None):
        self.name = name
        self.parent = parent
        self.files: List[Tuple[int, str]] = []
        self.subdirs: List["Dir"] = []

    def enter_subdir(self, name: str) -> "Dir":
        for subdir in self.subdirs:
            if subdir.name == name:
                return subdir
        raise NotImplementedError

    def parse_ls(self, cli_log: List[List[str]], index: int) -> int:
        while index < len(cli_log):
            parts = cli_log[index]
            if parts[0] == "$":
                break
            if parts[0] == "dir":
                self.subdirs.append(Dir(parts[1], self))
            else:
                self.files.append((int(parts[0]), parts[1]))
            index += 1
        return index

    def part_1(self) -> Tuple[int, int]:
        my_size = sum(size for size, _name in self.files)
        children_sizes: List[Tuple[int, int]] = [sd.part_1() for sd in self.subdirs]
        my_size += sum(child_size for child_size, _a in children_sizes)
        answer_total_so_far = sum(answer for _cs, answer in children_sizes)
        if my_size <= LARGEST_SIZE:
            answer_total_so_far += my_size
        return my_size, answer_total_so_far

    def part_2(self, candidates: List[int]) -> int:
        my_size = sum(size for size, _name in self.files)
        my_size += sum(sd.part_2(candidates) for sd in self.subdirs)
        candidates.append(my_size)
        return my_size


def solve(cli_log: List[List[str]]) -> Tuple[int, int]:
    cwd = root = None
    index = 0
    while index < len(cli_log):
        parts = cli_log[index]
        assert parts[0] == "$"
        if parts[1] == "cd":
            if parts[2] == "/":  # We're at root
                cwd = root = Dir("/")
            elif parts[2] == "..":
                cwd = cwd.parent
            else:
                cwd = cwd.enter_subdir(parts[2])
            index += 1
        if parts[1] == "ls":
            index = cwd.parse_ls(cli_log, index + 1)

    candidates = []
    root_size = root.part_2(candidates)
    needed_size = PATCH_SIZE - (DISK_SIZE - root_size)

    return root.part_1()[1], min(c for c in candidates if c >= needed_size)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT_DATA = [[p for p in line.split()] for line in DATA.split("\n")]

    print(solve(INPUT_DATA))
