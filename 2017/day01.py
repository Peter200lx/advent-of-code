from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


def part_1(sequence: str) -> int:
    cur_num = sequence[-1]
    sum_seq = 0
    for num in sequence:
        if num == cur_num:
            sum_seq += int(num)
        else:
            cur_num = num

    return sum_seq


def part_2(sequence: str) -> int:
    sum_half = 0
    length = len(sequence)
    for i in range(length):
        next_i = (i + length // 2) % length
        if sequence[i] == sequence[next_i]:
            sum_half += int(sequence[i])

    return sum_half


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    print(part_1(DATA))
    print(part_2(DATA))
