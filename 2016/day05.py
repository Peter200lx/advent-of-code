from hashlib import md5
from typing import Iterable

EXAMPLE_DATA = "abc"
DATA = "uqwqemis"

CODE_LENGTH = 8
VALID_LOC = {str(i) for i in range(CODE_LENGTH)}


def hash_gen(salt: str, start_str: str = "00000") -> Iterable[str]:
    for i in range(100_000_000):
        to_encode = f"{salt}{i}"
        possible_hash = md5(to_encode.encode()).hexdigest()
        if possible_hash.startswith(start_str):
            print(f"{to_encode} --hash-> {possible_hash}")
            yield possible_hash


if __name__ == "__main__":
    code = ""
    complex_code = [None] * CODE_LENGTH
    for valid_hash in hash_gen(DATA):
        if len(code) < CODE_LENGTH:
            code += valid_hash[5]
            print(f"p1 code so far: {code}")
        if valid_hash[5] in VALID_LOC:
            code_loc = int(valid_hash[5])
            if complex_code[code_loc] is None:
                complex_code[code_loc] = valid_hash[6]
                print(f"p2 code so far: {''.join('_' if v is None else v for v in complex_code)}")
        if len(code) >= CODE_LENGTH and None not in complex_code:
            break

    print(f"--- Part 1 answer is: {code}")
    print(f"--- Part 2 answer is: {''.join(complex_code)}")
