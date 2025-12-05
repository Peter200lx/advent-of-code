from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


def part1(ranges: list[range], ing_ids: list[int]) -> int:
    good = []
    for ing in ing_ids:
        for rang in ranges:
            if ing in rang:
                good.append(ing)
                break
    return len(good)


def part2(ranges: list[range]) -> int:
    merged = []

    for interval in sorted(ranges, key=lambda x: (x.start, x.stop)):
        if not merged or merged[-1].stop < interval.start:
            merged.append(interval)
        else:
            merged[-1] = range(merged[-1].start, max(merged[-1].stop, interval.stop))

    return sum(len(r) for r in merged)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    RANGES_STRS, ING_STIRS = DATA.split("\n\n")
    RANGES = [
        range(int(l), int(r) + 1)
        for line in RANGES_STRS.split("\n")
        for l, r in [line.split("-")]
    ]
    ING_IDS = [int(line) for line in ING_STIRS.split("\n")]

    print(part1(RANGES, ING_IDS))
    print(part2(RANGES))
