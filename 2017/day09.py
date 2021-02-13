from typing import Tuple, List
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

TEST_DATA = {
    "{}": 1,
    "{{{}}}": 6,
    "{{},{}}": 5,
    "{{{},{},{{}}}}": 16,
    "{<a>,<a>,<a>,<a>}": 1,
    "{{<ab>},{<ab>},{<ab>},{<ab>}}": 9,
    "{{<!!>},{<!!>},{<!!>},{<!!>}}": 9,
    "{{<a!>},{<a!>},{<a!>},{<ab>}}": 3,
    "{{<!>},{<!>},{<!>},{<a>}}": 3,
    "{<!!!>>}": 1,
    "{<{},{},{{}}>}": 1,
}


def find_end_of_garbage(garbage: str, i: int) -> Tuple[int, int]:
    i += 1  # Skip opening '<'
    garbage_count = 0
    while i < len(garbage):
        if garbage[i] == "!":
            i += 2
            continue
        elif garbage[i] == ">":
            return i + 1, garbage_count
        else:
            garbage_count += 1
            i += 1
    raise Exception(f"Garbage string never terminated\n{garbage}")


def parse_group(group: str, i: int) -> Tuple[int, List[List], int]:
    i += 1  # Skip opening '{'
    my_list = []
    garbage_count = 0
    while i < len(group):
        # print(group[i:])
        if group[i] == "<":
            i, sub_garbage_count = find_end_of_garbage(group, i)
            garbage_count += sub_garbage_count
        elif group[i] == "{":
            i, sub_list, sub_garbage_count = parse_group(group, i)
            garbage_count += sub_garbage_count
            my_list.append(sub_list)
        elif group[i] == "}":
            return i + 1, my_list, garbage_count
        else:
            i += 1
    raise Exception(f"Group string never terminated\n{group}")


def calc_score(g_list: List[List], depth: int = 1) -> int:
    score = depth
    for sub_list in g_list:
        score += calc_score(sub_list, depth + 1)
    return score


def run_p1_test():
    for input_str, result in TEST_DATA.items():
        i, test_list, _garbage_count = parse_group(input_str, 0)
        if i != len(input_str):
            print(f"-TEST- Finished processing at {i}, string length is {len(input_str)}")

        score = calc_score(test_list)
        if score != result:
            print(f"-TEST- Input_str {input_str} gave list {test_list}")
            print(f"-TEST- Score is {score}, should be {result}")


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    run_p1_test()
    _, DATA_LIST, GARBAGE_COUNT = parse_group(DATA, 0)
    print(f"Score is {calc_score(DATA_LIST)}")
    print(f"Garbage Count is {GARBAGE_COUNT}")
