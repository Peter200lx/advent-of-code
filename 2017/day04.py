from collections import Counter
from typing import List
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


def part_1(phrases: List[List[str]]) -> int:
    valid = 0
    for phrase in phrases:
        counter = Counter(phrase)
        if counter.most_common(1)[0][1] == 1:
            valid += 1
    return valid


def part_2(phrases: List[List[str]]) -> int:
    valid = 0
    for phrase in phrases:
        letters_list = set()
        valid_phrase = True
        for word in phrase:
            counter = Counter(word)
            letters = tuple(sorted(counter.most_common()))
            if letters in letters_list:
                valid_phrase = False
                break
            letters_list.add(letters)
        if valid_phrase:
            valid += 1
    return valid


def part_2_comprehension(phrases: List[List[str]]) -> int:
    valid = 0
    for phrase in phrases:
        counter = Counter(("".join(sorted(w)) for w in phrase))
        if counter.most_common(1)[0][1] == 1:
            valid += 1
    return valid


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    PHRASES = [[word for word in line.split()] for line in DATA.split("\n")]

    print(part_1(PHRASES))
    print(part_2(PHRASES))
    print(part_2_comprehension(PHRASES))
