from typing import List, Optional, Union

DATA = """cqjxjnds"""

BAD_LETTERS = {"i", "o", "l"}


def valid_password(seq: Union[str, List[str]]) -> bool:
    tri_seq = 0
    pair_1 = None
    pair_2 = None
    last: Optional[str] = None
    for i, c in enumerate(seq):
        if c in BAD_LETTERS:
            return False
        if last == c:
            if pair_1 and i > pair_1 + 1:
                pair_2 = i
            elif pair_1 is None:
                pair_1 = i
        if last:
            if ord(c) - 1 == ord(last):
                tri_seq += 1
            elif tri_seq < 2:
                tri_seq = 0
        last = c
    return pair_1 and pair_2 and tri_seq >= 2


def find_next_valid(old_pwd: str) -> str:
    current = list(old_pwd)
    loc = -1
    while True:
        for loc in range(-1, -len(current), -1):
            current[loc] = chr(ord(current[loc]) + 1)
            if current[loc] in BAD_LETTERS:
                current[loc] = chr(ord(current[loc]) + 1)
                for reset_loc in range(loc + 1, 0):
                    current[reset_loc] = "a"
                break
            if current[loc] <= "z":
                break
            current[loc] = "a"
        if valid_password(current):
            return "".join(current)


if __name__ == "__main__":
    assert valid_password("abcdffaa")
    assert find_next_valid("abcdefgh") == "abcdffaa"
    PART_1 = find_next_valid(DATA)
    print(PART_1)
    print(find_next_valid(PART_1))
