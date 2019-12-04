from collections import Counter


def validate(code, p2=False):
    if len(code) != 6:
        return False
    prev = 0
    for char in code:
        cur = int(char)
        if cur < prev:
            return False
        prev = cur
    c = Counter(code)
    return any(v > 1 if not p2 else v == 2 for v in c.values())


if __name__ == "__main__":
    DATA = "372037-905157"
    start, end = [int(num) for num in DATA.split("-")]
    print(sum(validate(str(n)) for n in range(start, end + 1)))
    print(sum(validate(str(n), p2=True) for n in range(start, end + 1)))
