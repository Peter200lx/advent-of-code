import re
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

MUL = re.compile(r"mul\((?P<d1>\d{1,3}),(?P<d2>\d{1,3})\)")
ANY = re.compile(r"(mul\((?P<d1>\d{1,3}),(?P<d2>\d{1,3})\)|do\(\)|don't\(\))")


def p2(prog: str) -> int:
    summ = index = 0
    enabled = True
    while index < len(prog):
        match = ANY.search(prog[index:])
        if match:
            index += match.start()
            if match.group() == "do()":
                enabled = True
            elif match.group() == "don't()":
                enabled = False
            elif enabled:
                summ += int(match.group("d1")) * int(match.group("d2"))
        index += 1
    return summ


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    print(sum(int(match[0]) * int(match[1]) for match in MUL.findall(DATA)))
    print(p2(DATA))
