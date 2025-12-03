from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


def parse_seq(pair_list: list[tuple[int, ...]]) -> int:
    to_power = []
    for seq in pair_list:
        first = -1, -1
        for i in range(0, len(seq) - 1):
            if seq[i] > first[1]:
                first = (i, seq[i])
        second = first[0] + 1, seq[first[0] + 1]
        for i in range(second[0], len(seq)):
            if seq[i] > second[1]:
                second = (i, seq[i])
        to_power.append(first[1] * 10 + second[1])
    return sum(to_power)


def part_two(pair_list: list[tuple[int, ...]], length=12) -> int:
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
    INPUT = [tuple(int(c) for c in line.strip("\n")) for line in DATA.split("\n")]

    print(parse_seq(INPUT))
    print(part_two(INPUT))
