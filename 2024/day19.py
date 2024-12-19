from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


def part1(patterns: list[str], designs: list[str]) -> int:
    valid_count = 0
    for design in designs:
        possible = [pat for pat in patterns if design.startswith(pat)]
        while possible:
            attempt = possible.pop()
            if len(attempt) == len(design):
                valid_count += 1
                break
            elif len(attempt) > len(design):
                break
            for pattern in patterns:
                if design[len(attempt) :].startswith(pattern):
                    possible.append(attempt + pattern)
    return valid_count


def part2(patterns: list[str], designs: list[str]) -> int:
    valid_count = 0
    for design in designs:
        possible = {pat: 1 for pat in patterns if design.startswith(pat)}
        valid_designs = 0
        while possible:
            attempt_str: str = min(possible.keys(), key=lambda x: len(x))
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
    return valid_count


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    PAT_STR, DES_STR = DATA.split("\n\n")
    PATTERNS = list(PAT_STR.split(", "))
    DESIGNS = list(DES_STR.split("\n"))

    print(part1(PATTERNS, DESIGNS))
    print(part2(PATTERNS, DESIGNS))
