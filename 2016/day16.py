from typing import List

DATA = """10111100110001111"""
PART_1 = 272
PART_2 = 35651584


def fill_disk(start_seq: List[bool], disk_size) -> List[bool]:
    seq = start_seq
    while len(seq) < disk_size:
        seq += [False] + [not b for b in reversed(seq)]
    return seq[:disk_size]


def checksum(disk: List[bool]) -> List[bool]:
    while len(disk) % 2 == 0:
        disk = [disk[i] == disk[i + 1] for i in range(0, len(disk), 2)]
    return disk


if __name__ == "__main__":
    START_SEQ = [c == "1" for c in DATA]
    RAW_DISK = fill_disk(START_SEQ, PART_1)
    CHECKSUM = checksum(RAW_DISK)
    print("".join("1" if b else "0" for b in CHECKSUM))
    print("".join("1" if b else "0" for b in checksum(fill_disk(START_SEQ, PART_2))))
