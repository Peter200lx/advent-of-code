import string
from pathlib import Path

FILE_DIR = Path(__file__).parent


def react(polymer):
    cur_pol = polymer
    i = 0
    while i < len(cur_pol) - 1:
        if cur_pol[i] != cur_pol[i + 1] and cur_pol[i].lower() == cur_pol[i + 1].lower():
            cur_pol = cur_pol[:i] + cur_pol[i + 2 :]
            i = max(i - 1, 0)
        else:
            i += 1
    return cur_pol


def part_2(polymer, max_len):
    best_len = (None, max_len)
    for c in string.ascii_lowercase:
        new_p = polymer.replace(c, "").replace(c.upper(), "")
        best = react(new_p)
        if len(best) < best_len[1]:
            best_len = (c, len(best))
    return best_len


if __name__ == "__main__":
    DATA = (FILE_DIR / "day05.input").read_text().strip()
    p1_len = len(react(DATA))
    print(p1_len)
    print(part_2(DATA, p1_len))
