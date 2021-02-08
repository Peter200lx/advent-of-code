from pathlib import Path
from pprint import pprint
from typing import List, Dict, Union

FILE_DIR = Path(__file__).parent

SCRAMBLE_START = "abcdefgh"
ALREADY_SCRAMBLED = "fbgdceah"


def interpret_moves(instructions: str, start: str = SCRAMBLE_START) -> str:
    cur_str: List[str] = list(start)
    reverse_map: Dict[int, List[List[Union[str, int]]]] = {n: [] for n in range(len(start))}
    for line in instructions.split("\n"):
        reverse_debug = None
        words = line.split()
        if not words:
            continue
        if words[0] == "swap":
            if words[1] == "position":
                ind_x, ind_y = int(words[2]), int(words[5])
            elif words[1] == "letter":
                x, y = words[2], words[5]
                ind_x, ind_y = cur_str.index(x), cur_str.index(y)
            else:
                raise NotImplementedError
            cur_str[ind_x], cur_str[ind_y] = cur_str[ind_y], cur_str[ind_x]
        elif words[0] == "rotate":
            if words[1] == "left":
                steps = int(words[2])
            elif words[1] == "right":
                steps = -int(words[2])
            elif words[1] == "based":
                based_on = words[6]
                ind_base = cur_str.index(based_on)
                reverse_debug = ["".join(cur_str), based_on]
                reverse_map[ind_base].append(reverse_debug)
                steps = -1 - ind_base
                if ind_base >= 4:
                    steps -= 1
            else:
                raise NotImplementedError
            steps %= len(cur_str)
            cur_str = cur_str[steps:] + cur_str[:steps]
            if reverse_debug:
                reverse_debug.extend(["".join(cur_str), cur_str.index(based_on), cur_str.index(based_on) - ind_base])
        elif words[0] == "reverse":
            x, y = int(words[2]), int(words[4])
            rev_stop = x - 1 if x - 1 >= 0 else None
            cur_str = cur_str[:x] + cur_str[y:rev_stop:-1] + cur_str[y + 1 :]
        elif words[0] == "move":
            x, y = int(words[2]), int(words[5])
            letter = cur_str[x]
            cur_str.remove(letter)
            cur_str.insert(y, letter)
        else:
            raise NotImplementedError
    # pprint(reverse_map)
    return "".join(cur_str)


REVERSE_MAP = {1: 1, 3: 2, 5: 3, 7: 4, 2: -2, 4: -1, 6: 0, 0: -7}


def reverse_scramble(instructions: str, end: str = ALREADY_SCRAMBLED) -> str:
    cur_str: List[str] = list(end)
    for line in reversed(instructions.split("\n")):
        words = line.split()
        if not words:
            continue
        if words[0] == "swap":  # ok
            if words[1] == "position":
                ind_x, ind_y = int(words[2]), int(words[5])
            elif words[1] == "letter":
                x, y = words[2], words[5]
                ind_x, ind_y = cur_str.index(x), cur_str.index(y)
            else:
                raise NotImplementedError
            cur_str[ind_x], cur_str[ind_y] = cur_str[ind_y], cur_str[ind_x]
        elif words[0] == "rotate":
            if words[1] == "left":  # ok
                steps = -int(words[2])
            elif words[1] == "right":  # ok
                steps = int(words[2])
            elif words[1] == "based":
                based_on = words[6]
                ind_base = cur_str.index(based_on)
                steps = REVERSE_MAP[ind_base]
            else:
                raise NotImplementedError
            steps %= len(cur_str)
            cur_str = cur_str[steps:] + cur_str[:steps]
        elif words[0] == "reverse":  # ok
            x, y = int(words[2]), int(words[4])
            rev_stop = x - 1 if x - 1 >= 0 else None
            cur_str = cur_str[:x] + cur_str[y:rev_stop:-1] + cur_str[y + 1 :]
        elif words[0] == "move":  # ok
            x, y = int(words[2]), int(words[5])
            letter = cur_str[y]
            cur_str.remove(letter)
            cur_str.insert(x, letter)
        else:
            raise NotImplementedError
    return "".join(cur_str)


if __name__ == "__main__":
    DATA = (FILE_DIR / "day21.input").read_text().strip()
    print(interpret_moves(DATA))
    print(reverse_scramble(DATA))
