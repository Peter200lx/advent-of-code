from typing import Tuple, FrozenSet, List

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


def build_full_room(current_traps: List[FrozenSet[int]], width: int, length: int) -> List[FrozenSet[int]]:
    for _ in range(len(current_traps), length):
        current_traps.append(next_row(current_traps[-1], width))
    return current_traps


if __name__ == "__main__":
    ROOM_WIDTH, ROOM_TRAPS = load_traps(DATA)
    PART1_TRAPS = build_full_room([ROOM_TRAPS], ROOM_WIDTH, PART1_LENGTH)
    print(sum(ROOM_WIDTH - len(traps) for traps in PART1_TRAPS))
    PART2_TRAPS = build_full_room(list(PART1_TRAPS), ROOM_WIDTH, PART2_LENGTH)
    print(sum(ROOM_WIDTH - len(traps) for traps in PART2_TRAPS))
