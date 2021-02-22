from hashlib import md5
from typing import Optional, Tuple

EXAMPLE_DATA = "abc"
DATA = "uqwqemis"

CODE_LENGTH = 8
VALID_LOC = {str(i) for i in range(CODE_LENGTH)}


def calc_digit(door_id: str, num: int) -> Optional[str]:
    mystr = f"{door_id}{num}"
    myhash = md5(mystr.encode("utf-8")).hexdigest()
    if myhash.startswith("00000"):
        print(f"{mystr} --hash-> {myhash}")
        return myhash[5]
    return None


def calc_digit2(door_id: str, num: int) -> Tuple[Optional[int], Optional[str]]:
    mystr = f"{door_id}{num}"
    myhash = md5(mystr.encode("utf-8")).hexdigest()
    if myhash[5] in VALID_LOC and myhash.startswith("00000"):
        print(f"{mystr} --hash-> {myhash}")
        return int(myhash[5]), myhash[6]
    return None, None


if __name__ == "__main__":
    code = ""
    for i in range(29999999):
        if i % 1_000_000 == 0:
            print(f"{i} currently >{code}<")
        code_val = calc_digit(DATA, i)
        if code_val is None:
            continue
        code += code_val
        if len(code) >= CODE_LENGTH:
            break

    print(f"--- Answer is: {code}\n\n")

    complex_code = [None] * CODE_LENGTH
    for i in range(29999999):
        if i % 1_000_000 == 0:
            print(f"{i} currently >{complex_code}<")
        code_loc, code_val = calc_digit2(DATA, i)
        if code_loc is None or complex_code[code_loc] is not None:
            continue
        complex_code[code_loc] = code_val
        if None not in complex_code:
            break

    print(f"--- Answer is: {''.join(complex_code)}")
