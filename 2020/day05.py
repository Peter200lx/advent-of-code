from math import ceil
from pathlib import Path
import re

FILE_DIR = Path(__file__).parent

ROWS = 128
SEATS = 8


def calculate_seat(line):
    row_dir, seat_dir = line[:7], line[7:]
    row_binary = row_dir.replace("F", "0").replace("B", "1")
    seat_binary = seat_dir.replace("L", "0").replace("R", "1")
    return int(row_binary, 2), int(seat_binary, 2)


def find_missing(seat_set):
    for seat in seat_set:
        if seat + 1 not in seat_set and seat + 2 in seat_set:
            return seat + 1
        elif seat - 1 not in seat_set and seat - 2 in seat_set:
            return seat - 1
    assert ValueError


if __name__ == "__main__":
    DATA = (FILE_DIR / "day05.input").read_text().strip()
    assert calculate_seat("FBFBBFFRLR") == (44, 5)
    assert calculate_seat("BFFFBBFRRR") == (70, 7)
    assert calculate_seat("FFFBBBFRRR") == (14, 7)
    assert calculate_seat("BBFFBBFRLL") == (102, 4)
    INPUT = {calculate_seat(line) for line in DATA.split("\n")}
    seat_sets = {r * 8 + s for r, s in INPUT}
    print(max(seat_sets))
    print(find_missing(seat_sets))
