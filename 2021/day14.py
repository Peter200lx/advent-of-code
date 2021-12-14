from collections import Counter
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


def generate_pairs(s: str) -> str:
    for i in range(len(s) - 1):
        yield s[i : i + 2]


def part1(s: str, rules_blob: str) -> int:
    rules = {
        first: first[0] + second + first[1]
        for line in rules_blob.split("\n")
        for first, second in [line.split(" -> ")]
    }
    for i in range(10):
        s = s[0] + "".join(rules.get(pair, pair)[1:] for pair in generate_pairs(s))
    c = Counter(s)
    return c.most_common()[0][1] - c.most_common()[-1][1]


def part2(s: str, rules_blob: str) -> int:
    rules = {
        first: (first[0] + second, second + first[1])
        for line in rules_blob.split("\n")
        for first, second in [line.split(" -> ")]
    }
    pair_count = Counter(generate_pairs(s))
    for i in range(40):
        new_count = Counter()
        for pair, count in pair_count.most_common():
            for new_pair in rules.get(pair, [pair]):
                new_count.update({new_pair: count})
        pair_count = new_count
    c = Counter(s[0])
    for letter, count in pair_count.most_common():
        c.update({letter[1]: count})
    return c.most_common()[0][1] - c.most_common()[-1][1]


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    TEMPLATE, RULES_BLOB = DATA.split("\n\n")
    print(part1(TEMPLATE, RULES_BLOB))
    print(part2(TEMPLATE, RULES_BLOB))
