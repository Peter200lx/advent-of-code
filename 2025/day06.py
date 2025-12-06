from math import prod
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


OPCODES = {"*": prod, "+": sum}


def parse(lines: list[str]) -> list[list[str]]:
    space_index = [
        i for i in range(len(lines[0])) if all(line[i] == " " for line in lines)
    ] + [None]
    problems = []
    num_start = 0
    for space in space_index:
        problems.append(
            [lines[i][num_start:space] for i in range(len(lines) - 1)]
            + [lines[-1][num_start:space].strip()]
        )
        if space:
            num_start = space + 1
    return problems


def part1(problems: list[list[str]]) -> int:
    return sum(OPCODES[p[-1]](int(n) for n in p[:-1]) for p in problems)


def part2(problems: list[list[str]]) -> int:
    return sum(
        OPCODES[p[-1]](int("".join(n[i] for n in p[:-1])) for i in range(len(p[0])))
        for p in problems
    )


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    PARSED = parse(DATA.split("\n"))

    print(part1(PARSED))
    print(part2(PARSED))
