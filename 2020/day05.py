from pathlib import Path

FILE_DIR = Path(__file__).parent


def calculate_seat(line):
    seat_binary = line.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1")
    return int(seat_binary, 2)


def find_missing(seat_set):
    for seat in seat_set:
        for n in (-1, 1):
            if seat + n not in seat_set and seat + 2 * n in seat_set:
                return seat + n
    assert ValueError


if __name__ == "__main__":
    DATA = (FILE_DIR / "day05.input").read_text().strip()
    assert calculate_seat("FBFBBFFRLR") == (44 * 8 + 5)
    assert calculate_seat("BFFFBBFRRR") == (70 * 8 + 7)
    assert calculate_seat("FFFBBBFRRR") == (14 * 8 + 7)
    assert calculate_seat("BBFFBBFRLL") == (102 * 8 + 4)
    SEATS = {calculate_seat(line) for line in DATA.split("\n")}
    print(max(SEATS))
    print(find_missing(SEATS))
