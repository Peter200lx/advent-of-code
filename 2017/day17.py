from typing import Tuple, List

NUMBER_REPS_P1 = 2017
NUMBER_REPS_P2 = 50000000

EXAMPLE_DATA = 3
DATA = 366


def build_list(num_steps: int, num_reps: int) -> Tuple[int, List[int]]:
    cur_loc = 0
    spin_list = [0]
    for i in range(1, num_reps + 1):
        cur_loc += num_steps + 1
        cur_loc %= len(spin_list)
        spin_list.insert(cur_loc, i)
    return cur_loc, spin_list


def track_1st_loc(num_steps: int, num_reps: int) -> int:
    cur_loc = 0
    loc_1st_val = 0
    for i in range(1, num_reps + 1):
        cur_loc = ((num_steps + cur_loc) % i) + 1
        if cur_loc == 1:
            loc_1st_val = i
    return loc_1st_val


if __name__ == "__main__":
    location, run_list = build_list(DATA, NUMBER_REPS_P1)
    print(run_list[location - 3 : location + 4])

    print(track_1st_loc(DATA, NUMBER_REPS_P2))
