from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

""" Version 1 of logic, got part 1 slowly
BASE_PATTERN = (0, 1, 0, -1)
BASE_LENGTH = len(BASE_PATTERN)


def build_pattern(position):
    base_index = 0
    first = True
    while True:
        for _ in range(position):
            if first:
                first = False
            else:
                yield BASE_PATTERN[base_index]
        base_index = (base_index + 1) % BASE_LENGTH


def run_phase(signal):
    return [
        abs(sum(n * p for n, p in zip(signal, build_pattern(i + 1)))) % 10
        for i in range(len(signal))
    ]
"""


def build_slices(length, limit):
    start = length
    sign = 1
    while start <= limit:
        e = start + length - 1
        if e > limit:
            yield sign, slice(start - 1, None)
        else:
            yield sign, slice(start - 1, e)
        sign *= -1
        start += 2 * length


def run_phase_slicing(signal):
    num_items = len(signal)
    """Commented out code replaced w/ list comprehension once working
    result_list = []
    for i in range(num_items):
        n = 0
        for sign, active_slice in build_slices(i + 1, num_items):
            # print(sign, signal[active_slice])
            n += sum(signal[active_slice]) * sign
        result_list.append(abs(n) % 10)
        # print(f"Final number {result_list[-1]}")
    return result_list
    """
    return [
        abs(sum(m * sum(signal[s]) for m, s in build_slices(i + 1, num_items))) % 10
        for i in range(num_items)
    ]


def run_phase_slicing_p2(signal, ignore_before):
    num_items = len(signal)
    return [0] * ignore_before + [
        abs(sum(m * sum(signal[s]) for m, s in build_slices(i + 1, num_items))) % 10
        for i in range(ignore_before, num_items)
    ]


def magic_logic(signal):
    # This is created using patterns that were noticed by others and recorded at:
    # https://www.reddit.com/r/adventofcode/comments/ebai4g/2019_day_16_solutions/fb3lts9/
    num_items = len(signal)
    ret_list = signal[:]
    for i in range(num_items - 2, -1, -1):
        ret_list[i] = (signal[i] + ret_list[i + 1]) % 10
    return ret_list


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    int_list = [int(c) for c in DATA]

    p1_list = int_list[:]
    for _ in range(100):
        p1_list = run_phase_slicing(p1_list)
    print("".join((str(i) for i in p1_list[:8])))

    offset = int("".join(str(i) for i in int_list[:7]))
    insane_list = int_list * 10_000
    assert offset > (len(insane_list) // 2)
    insane_list = insane_list[offset:]

    for _ in range(100):
        # Wrote run_phase_slicing_p2 myself, ~7.5min per phase on laptop
        # This works on all three examples, would give right answer if
        # run for a bit over 12 hours.
        # insane_list = run_phase_slicing_p2(insane_list, offset)
        # Ended up using magic logic found on reddit
        insane_list = magic_logic(insane_list)
    print("".join((str(i) for i in insane_list[:8])))
