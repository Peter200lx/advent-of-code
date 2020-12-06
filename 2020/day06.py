from pathlib import Path

FILE_DIR = Path(__file__).parent


def combine_groups(list_set):
    s = list_set[0]
    for item in list_set:
        s &= item
    return s


if __name__ == "__main__":
    DATA = (FILE_DIR / "day06.input").read_text().strip()
    ANSWERS = [[{c for c in person} for person in group.split("\n")] for group in DATA.split("\n\n")]
    print(sum(len({c for p in g for c in p}) for g in ANSWERS))
    print(sum(len(combine_groups(g)) for g in ANSWERS))
