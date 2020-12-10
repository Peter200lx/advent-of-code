from pathlib import Path

FILE_DIR = Path(__file__).parent


def part_1(all_adapters):
    diffs = {1: 0, 2: 0, 3: 1}
    current_v = 0
    for i, n in enumerate(sorted(all_adapters)):
        assert 0 < n - current_v <= 3
        diffs[n - current_v] += 1
        current_v = n
    print(diffs[3] * diffs[1])


def find_next_3_away(subset_adapters):
    last_n = subset_adapters[0]
    for i, cur_n in enumerate(subset_adapters):
        if cur_n - last_n == 3:
            return i
        last_n = cur_n
    return len(subset_adapters)


def find_combs(range_adapters, last_n):
    if len(range_adapters) == 1:
        return 1 if range_adapters[0] - last_n <= 3 else 0

    this_level = 0
    if range_adapters[0] - last_n <= 3:
        this_level += find_combs(range_adapters[1:], last_n)
    this_level += find_combs(range_adapters[1:], range_adapters[0])
    return this_level


def find_all_patterns(all_adapters):
    sorted_adapters = sorted(all_adapters)
    combinations = 1
    cur_n = 0
    i = 0
    while i < len(sorted_adapters):
        if sorted_adapters[i] - cur_n == 3:
            cur_n = sorted_adapters[i]
            i += 1
            continue
        end_i = i + find_next_3_away(sorted_adapters[i:])
        sub_combs = find_combs(sorted_adapters[i:end_i], cur_n)
        combinations *= sub_combs
        cur_n = sorted_adapters[end_i - 1]
        i = end_i
    return combinations


if __name__ == "__main__":
    DATA = (FILE_DIR / "day10.input").read_text().strip()
    NUMBERS = [int(i) for i in DATA.split("\n")]
    part_1(NUMBERS)
    print(find_all_patterns(NUMBERS))
