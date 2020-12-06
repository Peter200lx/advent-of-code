from pathlib import Path

FILE_DIR = Path(__file__).parent


if __name__ == "__main__":
    DATA = (FILE_DIR / "day06.input").read_text().strip()
    ANSWERS = [[{c for c in person} for person in group.split("\n")] for group in DATA.split("\n\n")]
    print(sum(len(set.union(*g)) for g in ANSWERS))
    print(sum(len(set.intersection(*g)) for g in ANSWERS))
