from pathlib import Path

FILE_DIR = Path(__file__).parent


def count_match(input: str, start=0) -> int:
    current = start
    first = True
    for i, char in enumerate(input, start=1):
        if char == "(":
            current += 1
        elif char == ")":
            current -= 1
        if current == -1 and first:
            print(i)
            first = False
    return current


if __name__ == "__main__":
    DATA = (FILE_DIR / "day01.input").read_text().strip()
    print(count_match(DATA))
