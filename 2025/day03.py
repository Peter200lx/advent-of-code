from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


def solve(pair_list: list[tuple[int, ...]], length=2) -> int:
    to_power = []
    for seq in pair_list:
        items = []
        start_index = 0
        for depth in range(length):
            max_for_depth = -1
            for i in range(start_index, len(seq) - (length - depth - 1)):
                if seq[i] > max_for_depth:
                    start_index = i
                    max_for_depth = seq[i]
            items.append(max_for_depth)
            start_index += 1
        to_power.append(sum(n * 10 ** (length - i - 1) for i, n in enumerate(items)))
    return sum(to_power)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT = [tuple(int(c) for c in line) for line in DATA.split("\n")]

    print(solve(INPUT))
    print(solve(INPUT, length=12))
