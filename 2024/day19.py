from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

def solve(patterns: list[str], designs: list[str]) -> tuple[int, int]:
    part1_count = 0
    valid_count = 0
    for design in designs:
        possible = {pat: 1 for pat in patterns if design.startswith(pat)}
        valid_designs = 0
        while possible:
            attempt_str: str = min(possible, key=lambda x: len(x))
            attempt_count = possible.pop(attempt_str)
            if len(attempt_str) == len(design):
                valid_designs += attempt_count
            elif len(attempt_str) > len(design):
                break
            for pattern in patterns:
                if design[len(attempt_str) :].startswith(pattern):
                    next_str = attempt_str + pattern
                    if next_str in possible:
                        possible[next_str] += attempt_count
                    else:
                        possible[next_str] = attempt_count
        valid_count += valid_designs
        if valid_designs:
            part1_count+=1
    return part1_count, valid_count


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    PAT_STR, DES_STR = DATA.split("\n\n")
    PATTERNS = list(PAT_STR.split(", "))
    DESIGNS = list(DES_STR.split("\n"))

    print("\n".join(str(n) for n in solve(PATTERNS, DESIGNS)))
