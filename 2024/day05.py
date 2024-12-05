from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


def is_valid(rules: dict, update: list[int], update_vals: set[int]) -> bool:
    for r_set, r_seq in rules.items():
        if len(update_vals & r_set) == 2:
            if update.index(r_seq[0]) > update.index(r_seq[1]):
                return False
    return True


def p1(rules: dict, updates: list[list[int]]) -> int:
    return sum(
        update[len(update) // 2]
        for update in updates
        if is_valid(rules, update, set(update))
    )


def p2(rules: dict, updates: list[list[int]]) -> int:
    count = 0
    for update in updates:
        update_vals = set(update)
        if not is_valid(rules, update, update_vals):
            while True:
                for r_set, r_seq in rules.items():
                    if len(update_vals & r_set) == 2:
                        i1, i2 = update.index(r_seq[0]), update.index(r_seq[1])
                        if i1 > i2:
                            update[i1], update[i2] = update[i2], update[i1]
                if is_valid(rules, update, update_vals):
                    count += update[len(update) // 2]
                    break
    return count


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    RULES_STR, UPDATES_STR = DATA.split("\n\n")
    RULES = {
        frozenset((int(n1), int(n2))): (int(n1), int(n2))
        for line in RULES_STR.split("\n")
        for n1, n2 in [line.split("|")]
    }
    UPDATES = [[int(n) for n in line.split(",")] for line in UPDATES_STR.split()]

    print(p1(RULES, UPDATES))
    print(p2(RULES, UPDATES))
