import heapq
import re
from itertools import combinations, product
from pathlib import Path
from typing import List, Dict, Tuple

INPUT_FILE = Path(__file__).with_suffix(".input")

IN_PARSE = re.compile(
    r"Valve (?P<name>\w+) has flow rate=(?P<rate>\d+); tunnels? leads? to valves? (?P<to>[A-Z, ]+)"
)

P1_TIME = 30
P2_TIME = 26


def parse_lines(lines: str) -> Dict[str, "Valve"]:
    valve_list = [Valve(line) for line in lines.split("\n")]
    valves = {v.name: v for v in valve_list}
    power = 0
    for valve in valve_list:
        valve.pow = 2**power
        power += 1
        for other_name in valve.to_valves:
            valve.tunnels.append(valves[other_name])
    return valves


class Valve:
    def __init__(self, raw: str):
        match = IN_PARSE.match(raw)
        self.name = match["name"]
        self.rate = int(match["rate"])
        self.to_valves = match["to"].split(", ")
        self.tunnels: List["Valve"] = []
        self.pow: int = 0

    def __lt__(self, other: "Valve"):
        return self.rate > other.rate


def get_int_distances(valves: Dict[str, Valve]) -> Dict[int, Dict[int, int]]:
    distance_count: Dict[int, Dict[int, int]] = {}
    for me in valves.values():
        me_dict = distance_count.setdefault(me.pow, {})
        me_dict[me.pow] = 0
        for other in me.tunnels:
            other_dict = distance_count.setdefault(other.pow, {})
            other_dict[me.pow] = 1
            me_dict[other.pow] = 1
    for a, b, c in product(distance_count, distance_count, distance_count):
        ac = distance_count[a].get(c, 9999)
        ab = distance_count[a].get(b, 9999)
        bc = distance_count[b].get(c, 9999)
        if ac + ab < bc:
            distance_count[b][c] = ac + ab
    return distance_count


def recursive_solve(
    distance: Dict[int, Dict[int, int]],
    rates: Dict[int, int],
    time_left: int,
    seen_valves: int,
    states: Dict[int, int],
    cur_valve: int,
    total: int = 0,
):
    if total > states.get(seen_valves, 0):
        states[seen_valves] = total
    for valve in rates:
        if valve & seen_valves:
            continue
        reduced_time = time_left - distance[cur_valve][valve] - 1
        if reduced_time < 0:
            continue
        updated_total = total + rates[valve] * reduced_time
        recursive_solve(
            distance,
            rates,
            reduced_time,
            seen_valves | valve,
            states,
            valve,
            updated_total,
        )


def part_1(valves: Dict[str, Valve], distance_count: [int, Dict[int, int]]) -> int:
    valve_rate = {v.pow: v.rate for v in valves.values() if v.rate}
    p1_cache = {}
    recursive_solve(distance_count, valve_rate, P1_TIME, 0, p1_cache, valves["AA"].pow)
    return max(p1_cache.values())


def part_2(valves: Dict[str, Valve], distance_count: [int, Dict[int, int]]) -> int:
    valve_rate = {v.pow: v.rate for v in valves.values() if v.rate}
    p2_cache = {}
    recursive_solve(distance_count, valve_rate, P2_TIME, 0, p2_cache, valves["AA"].pow)
    max_rate = 0
    interesting = 0
    for v in valve_rate:
        interesting |= v
    for (c1, v1), (c2, v2) in combinations(p2_cache.items(), 2):
        if (c1 & c2) == 0:
            if v1 + v2 > max_rate:
                max_rate = v1 + v2
            max_rate = max(max_rate, v1 + v2)

    return max_rate


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    VALVES = parse_lines(DATA)

    DISTANCES = get_int_distances(VALVES)

    print(part_1(VALVES, DISTANCES))
    print(part_2(VALVES, DISTANCES))
