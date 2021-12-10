from pathlib import Path
from statistics import median
from typing import List, Union

INPUT_FILE = Path(__file__).with_suffix(".input")

MATCHING = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}
REV_MATCH = {v: k for k, v in MATCHING.items()}

P1_SCORE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

P2_SCORE = {")": 1, "]": 2, "}": 3, ">": 4}


def collapse_errors(line: str) -> Union[str, int]:
    match_stack: List[str] = []
    for char in line:
        if char in MATCHING:
            match_stack.append(char)
        elif char in REV_MATCH:
            should_match = match_stack.pop()
            if should_match != REV_MATCH[char]:
                return P1_SCORE[char]
        else:
            raise NotImplementedError
    return "".join(reversed(match_stack))


def calc_p2_score(complete: str) -> int:
    score = 0
    for char in complete:
        score *= 5
        score += P2_SCORE[MATCHING[char]]
    return score


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    LINES = {collapse_errors(line) for line in DATA.split()}
    print(sum(err for err in LINES if isinstance(err, int)))
    print(median(calc_p2_score(comp) for comp in LINES if isinstance(comp, str)))
