from pathlib import Path
from typing import List, Tuple

FILE_DIR = Path(__file__).parent

MAX_32BIT = 4294967295


def parse_input(in_str: str) -> List[Tuple[int, int]]:
    ret_ranges = []
    for line in in_str.split("\n"):
        str1, str2 = line.split("-")
        ret_ranges.append((int(str1), int(str2)))
    return ret_ranges


def allowed_ips(blocked: List[Tuple[int, int]]) -> int:
    blocked = sorted(blocked)
    smallest_allowed = None
    allowed = 0
    cur_min = 0
    for min_ip, max_ip in blocked:
        if min_ip > cur_min:
            if smallest_allowed is None:
                smallest_allowed = cur_min
                print(smallest_allowed)
            allowed += min_ip - cur_min
        cur_min = max(cur_min, max_ip + 1)
    if cur_min < MAX_32BIT:
        allowed += MAX_32BIT - cur_min
    return allowed


if __name__ == "__main__":
    DATA = (FILE_DIR / "day20.input").read_text().strip()
    RANGES = parse_input(DATA)
    print(allowed_ips(RANGES))
