import heapq
import re
from itertools import combinations, product
from pathlib import Path
from typing import List, Dict, Tuple, Set, FrozenSet

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


def ideal_lost(total_so_far: int, time: int, max_flow_rate: int) -> int:
    return max_flow_rate * time - total_so_far


def part_1(valves: Dict[str, Valve], start_name: str = "AA") -> int:
    start = valves[start_name]
    valuable_valves = {v.name for v in valves.values() if v.rate}
    gfr = sum(v.rate for v in valves.values())  # greatest flow rate
    seen_states: Dict[Tuple[str, Tuple[str, ...]], int] = {}
    possible_paths: List[Tuple[int, int, int, int, Valve, List[str]]] = [
        (ideal_lost(0, 0, gfr), 0, 0, 0, start, [])
    ]
    max_so_far = 0
    if start.rate:
        heapq.heappush(
            possible_paths,
            (ideal_lost(0, 1, gfr), 0, 1, -start.rate, start, [start.name]),
        )
    while possible_paths:
        lost_value, inv_total, time, inv_rate, cur_loc, path_so_far = heapq.heappop(
            possible_paths
        )
        seen_so_far = {s for s in path_so_far if len(s) == 2}
        key = (cur_loc.name, tuple(sorted(seen_so_far)))
        if seen_states.get(key, 999999) < lost_value:
            continue
        seen_states[key] = lost_value
        if seen_so_far == valuable_valves or time == P1_TIME:
            real_total = -inv_total
            if time < P1_TIME:
                real_total += (-inv_rate) * (P1_TIME - time)
            if real_total > max_so_far:
                max_so_far = real_total
                print(real_total, time, -inv_rate, len(path_so_far), path_so_far)
            break
        if cur_loc.name not in seen_so_far and cur_loc.name in valuable_valves:
            possible_paths.append(
                (
                    ideal_lost(-inv_total - inv_rate, time + 1, gfr),
                    inv_total + inv_rate,
                    time + 1,
                    inv_rate - cur_loc.rate,
                    cur_loc,
                    path_so_far + [cur_loc.name],
                )
            )
        for other in cur_loc.tunnels:
            possible_paths.append(
                (
                    ideal_lost(-inv_total - inv_rate, time + 1, gfr),
                    inv_total + inv_rate,
                    time + 1,
                    inv_rate,
                    other,
                    path_so_far + [f"{cur_loc.name}-{other.name}"],
                )
            )
    return max_so_far


def part_2_try(valves: Dict[str, Valve], start_name: str = "AA") -> int:
    start = valves[start_name]
    valuable_valves = 0
    for v in valves.values():
        if v.rate:
            valuable_valves |= v.pow
    print(f"{valuable_valves:020b}")
    gfr = sum(v.rate for v in valves.values())  # greatest flow rate
    seen_states: Dict[Tuple[int, int], int] = {}
    possible_paths: List[Tuple[int, int, int, int, Valve, Valve, int]] = [
        (ideal_lost(0, 0, gfr), 0, 0, 0, start, start, 0)
    ]
    max_so_far = 0
    if start.rate:
        heapq.heappush(
            possible_paths,
            (ideal_lost(0, 1, gfr), 0, 1, -start.rate, start, start, start.pow),
        )
    while possible_paths:
        (
            lost_value,
            inv_total,
            time,
            inv_rate,
            my_loc,
            e_loc,
            seen_so_far,
        ) = heapq.heappop(possible_paths)
        if seen_so_far == valuable_valves or time == P2_TIME:
            real_total = -inv_total
            if time < P2_TIME:
                real_total += (-inv_rate) * (P2_TIME - time)
            if real_total > max_so_far:
                max_so_far = real_total
                print(real_total, lost_value, time, -inv_rate, f"\t{seen_so_far:020b}")
            continue
        key = (my_loc.pow | e_loc.pow, seen_so_far)
        if seen_states.get(key, 999999) < lost_value:
            continue
        seen_states[key] = lost_value
        my_moves: List[Tuple[int, Valve]] = []
        e_moves: List[Tuple[int, Valve]] = []
        if my_loc.pow & seen_so_far == 0 and my_loc.pow & valuable_valves:
            my_moves.append((my_loc.rate, my_loc))
        for other in my_loc.tunnels:
            my_moves.append((0, other))
        if (
            e_loc.pow & seen_so_far == 0
            and e_loc.pow & valuable_valves
            and e_loc.pow != my_loc.pow
        ):
            e_moves.append((e_loc.rate, e_loc))
        for other in e_loc.tunnels:
            e_moves.append((0, other))
        for my_rate, my_new in my_moves:
            m_str = my_new.name if my_new == my_loc else f"{my_loc.name}-{my_new.name}"
            added_valves = my_new.pow if my_new == my_loc else 0
            for e_rate, e_new in e_moves:
                e_str = e_new.name if e_new == e_loc else f"{e_loc.name}-{e_new.name}"
                added_valves |= e_new.pow if e_new == e_loc else 0
                if e_str == m_str:
                    continue

                new_lost = ideal_lost(-inv_total - inv_rate, time + 1, gfr)
                new_seen_so_far = seen_so_far | added_valves
                key = (my_new.pow | e_new.pow, new_seen_so_far)
                if seen_states.get(key, 999999) < new_lost:
                    continue
                seen_states[key] = new_lost
                possible_paths.append(
                    (
                        new_lost,
                        inv_total + inv_rate,
                        time + 1,
                        inv_rate - my_rate - e_rate,
                        my_new,
                        e_new,
                        new_seen_so_far,
                    )
                )
    return max_so_far


def part_2_sweep(
    valves: Dict[str, Valve], vv_count: int, start_name: str = "AA"
) -> List[str]:
    start = valves[start_name]
    valuable_valves = {v.name for v in valves.values() if v.rate}
    gfr = sum(v.rate for v in valves.values())  # greatest flow rate
    seen_states: Dict[Tuple[str, Tuple[str, ...]], int] = {}
    possible_paths: List[Tuple[int, int, int, int, Valve, List[str]]] = [
        (ideal_lost(0, 0, gfr), 0, 0, 0, start, [])
    ]
    min_lost = 99999999999999999999
    best_path = []
    if start.rate:
        heapq.heappush(
            possible_paths,
            (ideal_lost(0, 1, gfr), 0, 1, -start.rate, start, [start.name]),
        )
    while possible_paths:
        lost_value, inv_total, time, inv_rate, cur_loc, path_so_far = heapq.heappop(
            possible_paths
        )
        seen_so_far = {s for s in path_so_far if len(s) == 2}
        key = (cur_loc.name, tuple(sorted(seen_so_far)))
        if seen_states.get(key, 999999) < lost_value:
            continue
        seen_states[key] = lost_value
        if len(seen_so_far) == vv_count or time == P2_TIME:
            real_total = -inv_total
            if time < P2_TIME:
                real_total += (-inv_rate) * (P2_TIME - time)
            if lost_value < min_lost:
                min_lost = lost_value
                print(real_total, time, -inv_rate, path_so_far)
                best_path = path_so_far
                continue
        if cur_loc.name not in seen_so_far and cur_loc.name in valuable_valves:
            possible_paths.append(
                (
                    ideal_lost(-inv_total - inv_rate, time + 1, gfr),
                    inv_total + inv_rate,
                    time + 1,
                    inv_rate - cur_loc.rate,
                    cur_loc,
                    path_so_far + [cur_loc.name],
                )
            )
        for other in cur_loc.tunnels:
            possible_paths.append(
                (
                    ideal_lost(-inv_total - inv_rate, time + 1, gfr),
                    inv_total + inv_rate,
                    time + 1,
                    inv_rate,
                    other,
                    path_so_far + [f"{cur_loc.name}-{other.name}"],
                )
            )
    return best_path


def part_2_separate(valves: Dict[str, Valve]) -> int:
    valve_rate = {v.name: v.rate for v in valves.values()}
    start_req = sum(1 for v in valves.values() if v.rate) // 2
    my_sweep = part_2_sweep(VALVES, start_req)
    if len(my_sweep) < P2_TIME:
        my_sweep += [""] * (P2_TIME - len(my_sweep))
    print(f"Clearing out seen rates in {my_sweep}")
    for step in my_sweep:
        if len(step) == 2:
            valves[step].rate = 0
    e_sweep = part_2_sweep(VALVES, start_req)
    if len(e_sweep) < P2_TIME:
        e_sweep += [""] * (P2_TIME - len(e_sweep))
    rate = total = 0
    for our_steps in zip(my_sweep, e_sweep):
        total += rate
        for step in our_steps:
            if len(step) == 2:
                rate += valve_rate[step]
    return total


def get_all_distances(valves: Dict[str, Valve]) -> Dict[str, Dict[str, int]]:
    distance_count: Dict[str, Dict[str, int]] = {}
    for me in valves.values():
        me_dict = distance_count.setdefault(me.name, {})
        me_dict[me.name] = 0
        for other in me.tunnels:
            other_dict = distance_count.setdefault(other.name, {})
            other_dict[other.name] = 0
            other_dict[me.name] = 1
            me_dict[other.name] = 1
    # while any(len(d) != len(valves) for d in distance_count.values()):
    #     for me_name, me_dict in distance_count.items():
    #         for other_name in tuple(me_dict):
    #             other_dict = distance_count[other_name]
    #             for third_name in other_dict.keys() - set(me_dict.keys()):
    #                 me_dict[third_name] = other_dict[third_name] + 1
    #                 distance_count[third_name][me_name] = other_dict[third_name] + 1
    for a, b, c in product(distance_count, distance_count, distance_count):
        ab = distance_count[a].get(b, 9999)
        bc = distance_count[b].get(c, 9999)
        ac = distance_count[a].get(c, 9999)
        if ab + bc < ac:
            distance_count[a][c] = ab + bc
            distance_count[c][a] = ab + bc
    for k in distance_count:
        for o in distance_count[k]:
            assert (
                distance_count[k][o] == distance_count[o][k]
            ), f"dc[{k}]{distance_count[k]}  dc[{o}]{distance_count[o]=}"
    return distance_count


def find_min_path(
    distances: Dict[str, Dict[str, int]],
    rates: Dict[str, int],
    chosen_pts: Set[str],
    max_time: int = P2_TIME,
) -> int:
    gfr = sum(rates[s] for s in chosen_pts)
    to_check: List[Tuple[int, int, int, str, List[str]]] = [
        (ideal_lost(0, 0, gfr), 0, 0, "AA", [])
    ]
    seen_states: Dict[Tuple[str, FrozenSet[str]], int] = {}
    while to_check:
        lost_value, inv_total, time, loc, path_so_far = heapq.heappop(to_check)
        seen_so_far = frozenset({s for s in path_so_far if s})
        key = (loc, seen_so_far)
        if time > max_time:
            continue
        if seen_states.get(key, 999999) < lost_value:
            continue
        seen_states[key] = lost_value
        if seen_so_far == chosen_pts or (
            (max_time - time)
            < min(distances[loc][o] for o in chosen_pts - seen_so_far) + 1
        ):
            cur_rate = sum(rates[s] for s in seen_so_far)
            print(
                f"tot_so_far={-inv_total}, rem_time={max_time-time}, "
                f"{cur_rate=}, tot={-inv_total + (max_time - time) * cur_rate}, {time=}, "
                f"{len(path_so_far)=} {path_so_far}"
            )
            print(f"{len(seen_so_far)=} {len(chosen_pts)=}")
            return -inv_total + (max_time - time) * gfr
        for other, dist in distances[loc].items():
            if other not in chosen_pts:
                continue
            if other in seen_so_far:
                continue
            new_time = time + dist + 1
            new_total = inv_total - (dist + 1) * sum(rates[s] for s in seen_so_far)
            heapq.heappush(
                to_check,
                (
                    ideal_lost(-new_total, new_time, gfr),
                    new_total,
                    new_time,
                    other,
                    path_so_far + [""] * dist + [other],
                ),
            )


def hacked_p1_for_p2(
    valves: Dict[str, Valve], valuable_valves: Set[str], max_time: int
) -> int:
    # print(f"SEARCHING BEST FOR {tuple(sorted(valuable_valves))}")
    gfr = sum(v.rate for v in valves.values())  # greatest flow rate
    seen_states: Dict[Tuple[str, Tuple[str, ...]], int] = {}
    possible_paths: List[Tuple[int, int, int, int, Valve, List[str]]] = [
        (ideal_lost(0, 0, gfr), 0, 0, 0, valves["AA"], [])
    ]
    max_so_far = 0
    while possible_paths:
        lost_value, inv_total, time, inv_rate, cur_loc, path_so_far = heapq.heappop(
            possible_paths
        )
        seen_so_far = {s for s in path_so_far if len(s) == 2}
        key = (cur_loc.name, tuple(sorted(seen_so_far)))
        if seen_states.get(key, 999999) < lost_value:
            continue
        seen_states[key] = lost_value
        if seen_so_far == valuable_valves or time == max_time:
            real_total = -inv_total
            if time < max_time:
                real_total += (-inv_rate) * (max_time - time)
            if real_total > max_so_far:
                max_so_far = real_total
                # print(lost_value, real_total, time, -inv_rate, len(path_so_far), seen_so_far, path_so_far)
            continue
        if cur_loc.name not in seen_so_far and cur_loc.name in valuable_valves:
            possible_paths.append(
                (
                    ideal_lost(-inv_total - inv_rate, time + 1, gfr),
                    inv_total + inv_rate,
                    time + 1,
                    inv_rate - cur_loc.rate,
                    cur_loc,
                    path_so_far + [cur_loc.name],
                )
            )
        for other in cur_loc.tunnels:
            possible_paths.append(
                (
                    ideal_lost(-inv_total - inv_rate, time + 1, gfr),
                    inv_total + inv_rate,
                    time + 1,
                    inv_rate,
                    other,
                    path_so_far + [f"{cur_loc.name}-{other.name}"],
                )
            )
    # print(f"BEST WAS {max_so_far}")
    return max_so_far


def part_2_separate_combos(valves: Dict[str, Valve]) -> int:
    print(
        hacked_p1_for_p2(
            valves,
            {v.name for v in valves.values() if v.rate},
            max_time=P1_TIME,
        )
    )
    half_count = sum(1 for v in valves.values() if v.rate) // 2
    half_combo: Dict[Tuple[str, ...], int] = {}
    all_val_valves = {v.name for v in valves.values() if v.rate}
    print(f"Calc half")
    for combo in combinations(all_val_valves, half_count):
        half_combo[combo] = hacked_p1_for_p2(valves, set(combo), P2_TIME)
    print(f"Calc best of half")
    max_rate = 0
    max_c1 = None
    max_c2 = None
    for (c1, v1), (c2, v2) in combinations(half_combo.items(), 2):
        if not (set(c1) & set(c2)):
            if v1 + v2 > max_rate:
                max_rate = v1 + v2
                max_c1 = c1
                max_c2 = c2
                print(max_rate, max_c1, max_c2)
            max_rate = max(max_rate, v1 + v2)
    print(max_rate, max_c1, max_c2)
    # half_minus_combo = {}
    # half_plus_combo = {}
    # print(f"Calc half_minus")
    # for combo in combinations(all_val_valves, half_count - 1):
    #     half_minus_combo[combo] = hacked_p1_for_p2(valves, set(combo), P2_TIME)
    # print(f"Calc half_plus")
    # for combo in combinations(all_val_valves, half_count + 1):
    #     half_plus_combo[combo] = hacked_p1_for_p2(valves, set(combo), P2_TIME)
    # print(f"Calc best of plus/minus")
    # for hp_c, hp_v in half_plus_combo.items():
    #     hp_c_set = set(hp_c)
    #     for hm_c, hm_v in half_plus_combo.items():
    #         if hp_c_set | set(hm_c) == all_val_valves:
    #             # print(f"Checking {hm_v+hp_v=} {hm_v=} {hp_v=} {hm_c=}, {hp_c=}")
    #             if hm_v + hp_v > max_rate:
    #                 max_rate = hm_v + hp_v
    #                 max_c1 = hm_c
    #                 max_c2 = hp_c
    #                 print(max_rate, max_c1, max_c2)
    # print(max_c1, max_c2)

    return max_rate


def get_int_distances(valves: Dict[str, Valve]) -> Dict[int, Dict[int, int]]:
    distance_count: Dict[int, Dict[int, int]] = {}
    for me in valves.values():
        me_dict = distance_count.setdefault(me.pow, {})
        me_dict[me.pow] = 0
        for other in me.tunnels:
            other_dict = distance_count.setdefault(other.pow, {})
            other_dict[me.pow] = 1
            me_dict[other.pow] = 1
    # while any(len(d) != len(valves) for d in distance_count.values()):
    #     for me_name, me_dict in distance_count.items():
    #         for other_name in tuple(me_dict):
    #             other_dict = distance_count[other_name]
    #             for third_name in other_dict.keys() - set(me_dict.keys()):
    #                 me_dict[third_name] = other_dict[third_name] + 1
    #                 distance_count[third_name][me_name] = other_dict[third_name] + 1
    for a, b, c in product(distance_count, distance_count, distance_count):
        ac = distance_count[a].get(c, 9999)
        ab = distance_count[a].get(b, 9999)
        bc = distance_count[b].get(c, 9999)
        if ac + ab < bc:
            distance_count[b][c] = ac + ab
    for k in distance_count:
        for o in distance_count:
            assert (
                distance_count[k][o] == distance_count[o][k]
            ), f"dc[{k}]{distance_count[k]}  dc[{o}]{distance_count[o]=}"
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


def part_2(valves: Dict[str, Valve]) -> int:
    distance_count = get_int_distances(valves)
    valve_rate = {v.pow: v.rate for v in valves.values() if v.rate}
    p1_cache = {}
    print(f"starting")
    recursive_solve(distance_count, valve_rate, P1_TIME, 0, p1_cache, valves["AA"].pow)
    print(len(p1_cache))
    print("p1", max(p1_cache.values()))
    # half_count = len(valve_rate) // 2
    p2_cache = {}
    recursive_solve(distance_count, valve_rate, P2_TIME, 0, p2_cache, valves["AA"].pow)
    print(len(p2_cache))
    # p2_half = {k:v for k, v in p2_cache.items() if bin(k).count("1") == half_count}
    max_rate = 0
    max_c1 = None
    max_c2 = None
    interesting = 0
    for v in valve_rate:
        interesting |= v
    for (c1, v1), (c2, v2) in combinations(p2_cache.items(), 2):
        if (c1 & c2) == 0:
            if v1 + v2 > max_rate:
                max_rate = v1 + v2
                max_c1 = c1
                max_c2 = c2
                print(max_rate, max_c1, max_c2)
            max_rate = max(max_rate, v1 + v2)
    print(max_rate, max_c1, max_c2)

    return max_rate


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    VALVES = parse_lines(DATA)

    print(part_1(VALVES))
    print(part_2(VALVES))  # 2211 < answer < 2903  != 2588  != 2750 != 2749
