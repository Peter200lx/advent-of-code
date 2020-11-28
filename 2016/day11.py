import heapq
from datetime import datetime
from itertools import permutations

from typing import (
    List,
    Set,
    Tuple,
    NamedTuple,
    Iterator,
    FrozenSet,
    AbstractSet,
    Sequence,
)

"""The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant."""
EXAMPLE_DATA = [{"EE", "HM", "LM"}, {"HG"}, {"LG"}, set()]
EXAMPLE_PARTS = ["EE", "HG", "HM", "LG", "LM"]

"""The first floor contains a thulium generator, a thulium-compatible microchip, a plutonium generator, and a strontium generator.
The second floor contains a plutonium-compatible microchip and a strontium-compatible microchip.
The third floor contains a promethium generator, a promethium-compatible microchip, a ruthenium generator, and a ruthenium-compatible microchip.
The fourth floor contains nothing relevant."""
DATA = [{"EE", "TG", "TM", "PG", "SG"}, {"PM", "SM"}, {"OG", "OM", "RG", "RM"}, set()]
PARTS = ["EE", "TG", "TM", "PG", "PM", "SG", "SM", "OG", "OM", "RG", "RM"]


def print_board(board: Sequence[AbstractSet[str]], parts: Sequence[str]):
    print("         " + " :".join(parts) + " :")
    for i in range(len(board) - 1, -1, -1):
        floor_str = f"Floor {i} |"
        for obj in parts:
            floor_str += " X :" if obj in board[i] else " . :"
        print(floor_str)


def is_valid_floor(floor_set: AbstractSet[str]):
    generators = {g for g in floor_set if g[1] == "G"}
    if generators:
        for chip in (m for m in floor_set if m[1] == "M"):
            if f"{chip[0]}G" not in generators:
                return False
    return True


def is_valid_elevator(item_set: AbstractSet[str]) -> bool:
    if len(item_set) < 1 or len(item_set) > 2:
        return False
    return is_valid_floor(item_set)


def elevator_floor(board: Tuple[AbstractSet[str], ...]) -> int:
    return ["EE" in f for f in board].index(True)


class MoveException(Exception):
    pass


def move_elevator(building: Tuple[FrozenSet[str], ...], direction: str, item_set: Set[str]) -> Tuple[FrozenSet[str]]:
    if not is_valid_elevator(item_set):
        raise MoveException(f"Invalid contents for elevator (it would have {item_set}")
    cur_floor_num = elevator_floor(building)
    if (direction, cur_floor_num) == ("D", 0) or (direction, cur_floor_num) == ("U", len(building) - 1):
        raise MoveException(f"Can't move elevator {direction} when on the {cur_floor_num} floor")
    next_floor_num = cur_floor_num + (1 if direction == "U" else -1)
    if not building[cur_floor_num].issuperset(item_set):
        raise MoveException(f"Item(s) {item_set} are not all on current floor (here: {building[cur_floor_num]})")
    items_plus_elevator = {"EE", *item_set}
    cur_floor: FrozenSet[str] = frozenset(building[cur_floor_num] - items_plus_elevator)
    next_floor: FrozenSet[str] = frozenset(building[next_floor_num] | items_plus_elevator)
    if not is_valid_floor(cur_floor):
        raise MoveException(f"Current floor is invalid if elevator leaves (it would have {cur_floor}")
    if not is_valid_floor(next_floor):
        raise MoveException(f"next floor is invalid if elevator arrives (it would have {next_floor}")
    unlocked_building = list(building)
    unlocked_building[cur_floor_num] = cur_floor
    unlocked_building[next_floor_num] = next_floor
    return tuple(unlocked_building)


def hand_written(building: Tuple[AbstractSet[str]], item_list: Sequence[str]):
    moves = [
        ("U", {"PG", "SG"}),
        ("D", {"SM", "SG"}),
        ("U", {"TG", "SG"}),
        ("D", {"PM"}),
        ("U", {"PM", "TM"}),
        ("D", {"PM"}),
        ("U", {"PM", "SM"}),
        # Done with floor 0
        ("U", {"TG", "TM"}),
        ("U", {"TG", "TM"}),
        ("D", {"TG"}),
    ]
    print_board(building, item_list)
    for move in moves:
        print(move)
        building = move_elevator(building, *move)
        print_board(building, item_list)


class PriorityStates(NamedTuple):
    priority: int
    building: Tuple[FrozenSet[str]]


seen_buildings: Set[Tuple[FrozenSet[str]]] = set()
priority_states: List[PriorityStates] = []


def possible_moves_raw(building: Tuple[AbstractSet[str], ...]) -> Iterator[Tuple[str, FrozenSet[str]]]:
    current_floor = elevator_floor(building)
    possible_items = set(building[current_floor])
    possible_items.remove("EE")
    possible_combos = [(a,) for a in possible_items] + list(permutations(possible_items, 2))

    if current_floor == 0:
        directions = ("U",)
    elif current_floor == len(building):
        directions = ("D",)
    else:
        directions = ("U", "D")
    return ((d, frozenset(t)) for t in possible_combos for d in directions)


def find_moves(building: List[AbstractSet[str]], item_list: Sequence[str]):
    locked_building = tuple(frozenset(floor) for floor in building)
    heapq.heappush(priority_states, PriorityStates(0, locked_building))
    seen_buildings.add(locked_building)
    while True:
        next_move = heapq.heappop(priority_states)
        if next_move.building[-1].issuperset(item_list):
            print(f"Found destination in {next_move.priority} turns")
            return
        for instruction in possible_moves_raw(next_move.building):
            try:
                new_building = move_elevator(next_move.building, *instruction)
            except MoveException as e:
                # print(f"Instruction {next_move.move} failed with: {e}")
                # print_board(next_move.building, item_list)
                continue
            if new_building in seen_buildings:
                continue
            seen_buildings.add(new_building)
            heapq.heappush(priority_states, PriorityStates(next_move.priority + 1, new_building))


if __name__ == "__main__":
    # hand_written(DATA, PARTS)
    # find_moves(EXAMPLE_DATA, EXAMPLE_PARTS)
    start_time = datetime.now()
    find_moves(DATA, PARTS)
    p1_done_time = datetime.now()
    print(f"Part 1 Took {p1_done_time - start_time}")
    extra_parts = ["EG", "EM", "DG", "DM"]
    part2_data = list(DATA)
    part2_data[0] |= set(extra_parts)
    find_moves(part2_data, PARTS + extra_parts)
    print(f"Part 2 took {datetime.now() - p1_done_time}")
