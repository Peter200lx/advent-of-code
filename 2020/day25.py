import sys
from typing import Iterator, Tuple

DATA = """17115212
3667832"""


def yield_transform(subject_number: int) -> Iterator[Tuple[int, int]]:
    val = 1
    for i in range(sys.maxsize):
        yield i, val
        val *= subject_number
        val %= 20201227


def calc_private_key(pubkey1: int, pubkey2: int, double_check=False):
    loop1 = loop2 = None
    for i, val in yield_transform(7):
        if val == pubkey1:
            loop1 = i
            break
    if double_check:
        for i, val in yield_transform(7):
            if val == pubkey2:
                loop2 = i
                break
        for i, val in yield_transform(pubkey1):
            if i == loop2:
                print(val)
                break
    for i, val in yield_transform(pubkey2):
        if i == loop1:
            print(val)
            break


if __name__ == "__main__":
    PUBKEY1, PUBKEY2 = [int(line) for line in DATA.split("\n")]
    calc_private_key(PUBKEY1, PUBKEY2)
