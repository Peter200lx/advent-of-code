from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


def parse_pairs(pair_list: list[tuple[int, int]]) -> tuple[int, int]:
    invalids = []
    p2_invalids = []
    for left, right in pair_list:
        for num in range(left, right + 1):
            int_str = str(num)
            if len(int_str) % 2 == 0:
                half = len(int_str) // 2
                if int_str[:half] == int_str[half:]:
                    invalids.append(num)
            for i in range(1, len(int_str) // 2 + 1):
                cur = int_str[:i]
                for j in range(i, len(int_str), i):
                    if cur != int_str[j : j + i]:
                        break
                else:
                    p2_invalids.append(num)
                    break
    return sum(invalids), sum(p2_invalids)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INPUT = [(int(l), int(r)) for x in DATA.split(",") for l, r in [x.split("-")]]

    print("\n".join(str(n) for n in parse_pairs(INPUT)))
