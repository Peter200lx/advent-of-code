from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


def find_start(in_str: str, uniq_size: int) -> int:
    for i, c in enumerate(in_str):
        if len(set(in_str[i : i + uniq_size])) == uniq_size:
            return i + uniq_size


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    print(find_start(DATA, 4))
    print(find_start(DATA, 14))
