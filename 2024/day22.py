from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


PRUNE_NUM = 16777216

class SecretGen:
    def __init__(self, start_num: int):
        self.start = start_num
        self.iter_count = 0
        self.cur = start_num


    @staticmethod
    def next(cur: int):
        cur ^= cur * 64
        cur %= PRUNE_NUM
        cur ^= cur // 32
        cur %= PRUNE_NUM
        cur ^= cur * 2048
        cur %= PRUNE_NUM
        return cur

    def get_secret(self, iter_count: int):
        cur = self.start
        for _ in range(iter_count):
            cur = self.next(cur)
        return cur


def part2(gens: list[int]) -> int:
    seq_values = {}
    for secret in gens:
        cur_val = secret
        last_dig = cur_val % 10
        deltas = []
        seen = set()
        for i in range(2000):
            cur_val = SecretGen.next(cur_val)
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
    print(max(seq_values.items(), key=lambda x:x[1]))
    return max(seq_values.values())


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    GENS = [int(line) for line in DATA.split("\n")]

    print(sum(SecretGen(g).get_secret(2000) for g in GENS))
    print(part2(GENS))
