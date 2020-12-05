from pathlib import Path

FILE_DIR = Path(__file__).parent

TRANSLATOR = "".maketrans("FLBR", "0011")


if __name__ == "__main__":
    DATA = (FILE_DIR / "day05.input").read_text().strip()
    SEATS = {int(line.translate(TRANSLATOR), 2) for line in DATA.split("\n")}
    max_seat = max(SEATS)
    print(max_seat)
    print([x for x in range(min(SEATS), max_seat) if x not in SEATS])
