DATA = """34000000"""


def find_min(above: int, part_2=False):
    locs = [0] * (above // 10)
    for i in range(1, above // 10):
        visited = 0
        for j in range(i, above // 10, i):
            if part_2:
                locs[j] += 11 * i
                visited += 1
                if visited > 50:
                    break
            else:
                locs[j] += 10 * i
    return next(i for i, v in enumerate(locs) if v > above)


if __name__ == "__main__":
    MIN_PRES = int(DATA)
    print(find_min(MIN_PRES))
    print(find_min(MIN_PRES, part_2=True))
