from pathlib import Path

FILE_DIR = Path(__file__).parent


if __name__ == "__main__":
    DATA = (FILE_DIR / "day05.input").read_text().strip()
    SEATS = {
        int(line.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1"), 2)
        for line in DATA.split("\n")
    }
    max_seat = max(SEATS)
    print(max_seat)
    print([x for x in range(min(SEATS), max_seat) if x not in SEATS])
