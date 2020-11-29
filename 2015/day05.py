from pathlib import Path

VOWELS = "aeiou"

BAD_STRS = ("ab", "cd", "pq", "xy")


def is_good_str_p1(input: str) -> bool:
    # for bs in BAD_STRS:
    #     if bs in input:
    #         return False
    input_len = len(input)
    verb_count = 0
    found_dupe = False
    for i in range(input_len):
        if input[i] in VOWELS:
            verb_count += 1
        if i + 1 < input_len:
            if input[i : i + 2] in BAD_STRS:
                return False
            if input[i] == input[i + 1]:
                found_dupe = True
    return found_dupe and verb_count >= 3


def is_good_str_p2(input: str) -> bool:
    input_len = len(input)
    found_mirror = False
    pair_dict = {}
    found_pair_match = False
    for i in range(input_len):
        if i + 1 < input_len:
            pair = input[i : i + 2]
            if pair in pair_dict and pair_dict[pair] + 1 < i:
                found_pair_match = True
            if pair not in pair_dict:
                pair_dict[pair] = i
        if i + 2 < input_len:
            if input[i] == input[i + 2]:
                found_mirror = True
    return found_pair_match and found_mirror


if __name__ == "__main__":
    DATA = Path("day05.input").read_text().strip()
    INPUT_DATA = [s for s in DATA.split()]
    print((len([s for s in INPUT_DATA if is_good_str_p1(s)])))
    print((len([s for s in INPUT_DATA if is_good_str_p2(s)])))
