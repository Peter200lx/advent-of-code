from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

PART_1_CARDS = 10_007
PART_2_CARDS = 119_315_717_514_047
PART_2_SHUFFLE_REPEAT = 101_741_582_076_661


def part_1(inst_strs):
    run_list = list(range(PART_1_CARDS))
    for instruction in inst_strs:
        instruction = instruction.split()
        if instruction[1] == "into":
            run_list = list(reversed(run_list))
        elif instruction[1] == "with":
            increment = int(instruction[3])
            new_list = [-1] * PART_1_CARDS
            i = 0
            for val in run_list:
                new_list[i] = val
                i += increment
                i %= PART_1_CARDS
            run_list = new_list
        else:
            cut = int(instruction[1])
            run_list = run_list[cut:] + run_list[:cut]
    return run_list


def part_2(inst_strs, num_cards, repetitions, target):
    # Part 2 logic not designed myself, built after reading reddit solutions
    offset = 0
    increment = 1
    for instruction in inst_strs:
        instruction = instruction.split()
        if instruction[1] == "into":  # deal into new stack
            increment *= -1
            offset += increment
        elif instruction[1] == "with":  # deal with increment #int#
            inc_diff = int(instruction[3])
            increment *= pow(inc_diff, num_cards - 2, num_cards)
        else:  # cut #int#
            cut = int(instruction[1])
            offset += increment * cut
    offset *= pow(1 - increment, num_cards - 2, num_cards)
    increment = pow(increment, repetitions, num_cards)
    return (target * increment + (1 - increment) * offset) % num_cards


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip("\n")
    lines = DATA.split("\n")

    print(part_1(lines).index(2019))
    print(part_2(lines, PART_2_CARDS, PART_2_SHUFFLE_REPEAT, 2020))
