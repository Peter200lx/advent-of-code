from typing import Tuple, FrozenSet

DATA = """.^^^.^.^^^^^..^^^..^..^..^^..^.^.^.^^.^^....^.^...^.^^.^^.^^..^^..^.^..^^^.^^...^...^^....^^.^^^^^^^"""
PART1_LENGTH = 40
PART2_LENGTH = 400000


def load_traps(input_str: str) -> Tuple[int, FrozenSet[int]]:
    assert "\n" not in input_str
    return len(input_str), frozenset(x for x, c in enumerate(input_str) if c == "^")


def is_trap(known_traps: FrozenSet[int], new_loc: int) -> bool:
    left, center, right = [new_loc + shift in known_traps for shift in (-1, 0, 1)]
    if left and center and not right:
        return True
    if center and right and not left:
        return True
    if left and not center and not right:
        return True
    if right and not left and not center:
        return True
    return False


def next_row(prev_row: FrozenSet[int], width: int) -> FrozenSet[int]:
    return frozenset(x for x in range(width) if is_trap(prev_row, x))


def count_next_traps(last_row_traps: FrozenSet[int], width: int, length: int) -> Tuple[int, FrozenSet[int]]:
    safe_count = 0
    for _ in range(length):
        next_row_traps = next_row(last_row_traps, width)
        safe_count += width - len(next_row_traps)
        last_row_traps = next_row_traps
    return safe_count, last_row_traps


if __name__ == "__main__":
    ROOM_WIDTH, ROOM_TRAPS = load_traps(DATA)
    STARTING_SAFE = ROOM_WIDTH - len(ROOM_TRAPS)
    PART1_SAFE, PART1_TRAPS = count_next_traps(ROOM_TRAPS, ROOM_WIDTH, PART1_LENGTH - 1)
    print(STARTING_SAFE + PART1_SAFE)
    PART2_SAFE, PART2_TRAPS = count_next_traps(PART1_TRAPS, ROOM_WIDTH, PART2_LENGTH - PART1_LENGTH)
    print(STARTING_SAFE + PART1_SAFE + PART2_SAFE)
