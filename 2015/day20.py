DATA = """34000000"""


def find_min(above: int):
    locs = [0] * (above // 10)
    locs_p2 = [0] * (above // 10)
    for i in range(1, above // 10):
        visited = 0
        for j in range(i, above // 10, i):
            if visited <= 50:
                locs_p2[j] += 11 * i
                visited += 1
            locs[j] += 10 * i
    return tuple(next(i for i, v in enumerate(L) if v > above) for L in (locs, locs_p2))


if __name__ == "__main__":
    MIN_PRES = int(DATA)
    part_1, part_2 = find_min(MIN_PRES)
    print(part_1)
    print(part_2)
