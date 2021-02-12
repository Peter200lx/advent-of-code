from ast import literal_eval
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

if __name__ == "__main__":
    LINES = INPUT_FILE.read_text().strip().split("\n")
    DECODED = [literal_eval(s) for s in LINES]
    print(sum(len(s) for s in LINES) - sum(len(s) for s in DECODED))
    ENCODED = [s.translate(str.maketrans({"\\": "\\\\", '"': '\\"'})) for s in LINES]
    print(sum(len(s) + 2 for s in ENCODED) - sum(len(s) for s in LINES))
