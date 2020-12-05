from math import ceil
from pathlib import Path
import re

FILE_DIR = Path(__file__).parent

ROWS = 128
SEATS = 8


def calculate_seat(line):
    row_dir, seat_dir = line[:7], line[7:]
    min_row = 0
    max_row = ROWS - 1
    for c in row_dir:
        m = ceil((min_row + max_row) / 2)
        if c == "F":
            max_row = m - 1
        elif c == "B":
            min_row = m
    row = min_row
    min_seat = 0
    max_seat = SEATS - 1
    for c in seat_dir:
        m = ceil((min_seat + max_seat) / 2)
        if c == "L":
            max_seat = m - 1
        elif c == "R":
            min_seat = m
    seat = min_seat
    return row, seat


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
