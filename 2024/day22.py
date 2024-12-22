from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


PRUNE_NUM = 16777216


def next_sec(cur: int):
    cur ^= cur * 64
    cur %= PRUNE_NUM
    cur ^= cur // 32
    cur %= PRUNE_NUM
    cur ^= cur * 2048
    cur %= PRUNE_NUM
    return cur


def solve(gens: list[int]) -> tuple[int, int]:
    part1 = 0
    seq_values = {}
    for secret in gens:
        cur_val = secret
        last_dig = cur_val % 10
        deltas = []
        seen = set()
        for i in range(2000):
            cur_val = next_sec(cur_val)
            next_last_dig = cur_val % 10
            deltas.append(next_last_dig - last_dig)
            if len(deltas) >= 4:
                key = tuple(deltas[-4:])
                if key not in seen:
                    if key in seq_values:
                        seq_values[key] += next_last_dig
                    else:
                        seq_values[key] = next_last_dig
                seen.add(key)
            last_dig = next_last_dig
        part1 += cur_val
    return part1, max(seq_values.values())


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    GENS = [int(line) for line in DATA.split("\n")]

    print("\n".join(str(n) for n in solve(GENS)))
