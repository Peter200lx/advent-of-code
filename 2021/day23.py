import heapq
from pathlib import Path
from typing import NamedTuple, Dict, List, Optional, Tuple, Iterator

INPUT_FILE = Path(__file__).with_suffix(".input")

ROOMS = ["A", "B", "C", "D"]
HALLWAY_ROOM_ENTRANCES = {2: 0, 4: 1, 6: 2, 8: 3}
HALLWAY_ROOM_LOCS = {v: k for k, v in HALLWAY_ROOM_ENTRANCES.items()}
HALLWAY_LENGTH = 11
EMPTY_HALLWAY = "." * HALLWAY_LENGTH
COSTS = {"A": 1, "B": 10, "C": 100, "D": 1000}


def load_input(data: str):
    lines = data.split("\n")
    assert lines[0] == "#############"
    assert lines[1] == "#...........#"
    rooms = (
        (lines[2][3] + lines[3][3]),
        (lines[2][5] + lines[3][5]),
        (lines[2][7] + lines[3][7]),
        (lines[2][9] + lines[3][9]),
    )
    assert all(c in ("A", "B", "C", "D") for h in rooms for c in h)
    return rooms


class WorldState(NamedTuple):
    hallway: str  # assert len(hallway)==11
    rooms: Tuple[str, str, str, str]  # assert all(len(s) in (2, 4) for s in rooms)

    def match_ideal(self):
        if self.hallway != EMPTY_HALLWAY:
            return False
        for i, room in enumerate(self.rooms):
            if any(c != ROOMS[i] for c in room):
                return False
        return True

    def room_leave(self, num: int) -> Tuple[str, int, Optional[str]]:
        room = self.rooms[num]
        if any(c not in (".", ROOMS[num]) for c in room):
            for depth, c in enumerate(room):
                if c != ".":
                    return c, depth, room[:depth] + "." + room[depth + 1 :]
        return "", 0, None  # Nothing to move

    def hallway_leave(self) -> Iterator[Tuple[str, int, int, str]]:
        """Returns list of moves, where a move is:
        (letter moving, cost of move, room to enter, new hallway)
        """
        if all(c == "." for c in self.hallway):
            return []
        for loc, c in enumerate(self.hallway):
            if c == ".":
                continue
            new_hallway = self.hallway[:loc] + "." + self.hallway[loc + 1 :]
            if loc >= 3:
                for left in range(loc - 1, 1, -1):
                    if self.hallway[left] != ".":
                        break
                    if left in HALLWAY_ROOM_ENTRANCES:
                        yield c, loc - left, HALLWAY_ROOM_ENTRANCES[left], new_hallway
            if loc <= 7:
                for right in range(loc + 1, 9):
                    if self.hallway[right] != ".":
                        break
                    if right in HALLWAY_ROOM_ENTRANCES:
                        yield c, right - loc, HALLWAY_ROOM_ENTRANCES[right], new_hallway

    def hallway_enter(
        self, from_room: int, mover: str
    ) -> Iterator[Tuple[int, Optional[int], str]]:
        hallway_start = HALLWAY_ROOM_LOCS[from_room]
        for left in range(hallway_start - 1, -1, -1):
            if self.hallway[left] != ".":
                break
            if left in HALLWAY_ROOM_ENTRANCES:
                yield hallway_start - left + 1, HALLWAY_ROOM_ENTRANCES[
                    left
                ], self.hallway
            else:
                new_hallway = self.hallway[:left] + mover + self.hallway[left + 1 :]
                yield hallway_start - left + 1, None, new_hallway
        for right in range(hallway_start + 1, HALLWAY_LENGTH):
            if self.hallway[right] != ".":
                break
            if right in HALLWAY_ROOM_ENTRANCES:
                yield right - hallway_start + 1, HALLWAY_ROOM_ENTRANCES[
                    right
                ], self.hallway
            else:
                new_hallway = self.hallway[:right] + mover + self.hallway[right + 1 :]
                yield right - hallway_start + 1, None, new_hallway

    def room_enter(self, room_num: int, mover: str) -> Tuple[int, Optional[str]]:
        room_type = ROOMS[room_num]
        if mover != room_type:
            return 0, None  # mover can't enter this room
        if any(c not in (".", room_type) for c in self.rooms[room_num]):
            return 0, None  # Nothing can move in until all have moved out
        room = self.rooms[room_num]
        if room[0] == room_type:
            raise NotImplementedError(
                f"Why are we trying to move {room_type} into full room {room}!!"
            )
        deepest_open = 0
        for depth, c in enumerate(room):
            if c == ".":
                deepest_open = depth
        return (
            deepest_open + 1,
            room[:deepest_open] + mover + room[deepest_open + 1 :],
        )

    def yield_next(self) -> Iterator[Tuple[int, "WorldState"]]:
        for leave in range(len(self.rooms)):
            mover, leave_cost, departed_room = self.room_leave(leave)
            if departed_room is None:
                continue
            for h_cost, possible_room, new_hallway in self.hallway_enter(leave, mover):
                if possible_room is None:
                    rooms = list(self.rooms)
                    rooms[leave] = departed_room
                    yield COSTS[mover] * (leave_cost + h_cost), WorldState(
                        new_hallway, tuple(rooms)
                    )
                else:
                    enter_cost, new_enter_room = self.room_enter(possible_room, mover)
                    if new_enter_room:
                        rooms = list(self.rooms)
                        rooms[leave] = departed_room
                        rooms[possible_room] = new_enter_room
                        yield COSTS[mover] * (
                            leave_cost + h_cost + enter_cost
                        ), WorldState(new_hallway, tuple(rooms))
        for mover, h_cost, possible_room, new_hallway in self.hallway_leave():
            enter_cost, new_enter_room = self.room_enter(possible_room, mover)
            if new_enter_room:
                rooms = list(self.rooms)
                rooms[possible_room] = new_enter_room
                yield COSTS[mover] * (h_cost + enter_cost), WorldState(
                    new_hallway, tuple(rooms)
                )


def solve(starting_world: WorldState) -> int:
    seen_worlds: Dict[WorldState, int] = {}
    queue: List[Tuple[int, WorldState]] = []
    heapq.heappush(queue, (0, starting_world))
    while queue:
        cost, cur_world = heapq.heappop(queue)
        if seen_worlds.get(cur_world, 999999) <= cost:
            continue
        if cur_world.match_ideal():
            return cost
        seen_worlds[cur_world] = cost
        for new_cost, new_world in cur_world.yield_next():
            if seen_worlds.get(new_world, 999999) <= cost + new_cost:
                continue
            heapq.heappush(queue, (cost + new_cost, new_world))
    raise NotImplementedError


def part2(start: Tuple[str, str, str, str]) -> int:
    """Add
    #D#C#B#A#
    #D#B#A#C#
    """
    to_add = ("DD", "CB", "BA", "AC")
    start = tuple(start[i][0] + to_add[i] + start[i][-1] for i in range(4))
    starting_world = WorldState(EMPTY_HALLWAY, start)
    return solve(starting_world)


def part1(start: Tuple[str, str, str, str]) -> int:
    starting_world = WorldState(EMPTY_HALLWAY, start)
    return solve(starting_world)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    STARTING_ROOMS = load_input(DATA)
    print(part1(STARTING_ROOMS))
    print(part2(STARTING_ROOMS))
