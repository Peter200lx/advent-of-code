from collections import Counter
from pathlib import Path

FILE_DIR = Path(__file__).parent


def part1(lines):
    counters = [Counter(line[i] for line in lines) for i in range(len(lines[0]))]

    most = "".join(count.most_common()[0][0] for count in counters)
    least = "".join(count.most_common()[-1][0] for count in counters)
    return most, least


def part2(lines):
    oxy_pool = co2_pool = lines
    for i in range(len(lines[0])):
        if len(oxy_pool) > 1:
            oxy_mc = Counter(l[i] for l in oxy_pool).most_common()
            oxy_digit = "1" if oxy_mc[0][1] == oxy_mc[1][1] else oxy_mc[0][0]
            oxy_pool = [l for l in oxy_pool if l[i] == oxy_digit]
        if len(co2_pool) > 1:
            co2_mc = Counter(l[i] for l in co2_pool).most_common()
            co2_digit = "0" if co2_mc[0][1] == co2_mc[1][1] else co2_mc[-1][0]
            co2_pool = [l for l in co2_pool if l[i] == co2_digit]
    return oxy_pool[0], co2_pool[0]


if __name__ == "__main__":
    DATA = (FILE_DIR / "day03.input").read_text().strip()
    INPUT = [i for i in DATA.split("\n")]

    MOST_COMMON, LEAST_COMMON = part1(INPUT)

    print(int(MOST_COMMON, base=2) * int(LEAST_COMMON, base=2))

    OXY_RATING, CO2_RATING = part2(INPUT)
    print(int(OXY_RATING, base=2) * int(CO2_RATING, base=2))
