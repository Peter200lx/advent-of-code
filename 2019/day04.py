from collections import Counter


def validate(code, p2=False):
    if len(code) != 6:
        return False
    prev = "0"
    for char in code:
        if char < prev:
            return False
        prev = char
    c = Counter(code)
    return any(v > 1 if not p2 else v == 2 for v in c.values())


if __name__ == "__main__":
    DATA = "372037-905157"
    start, end = [int(num) for num in DATA.split("-")]
    valid_nums_p1 = [n for n in range(start, end + 1) if validate(str(n))]
    print(len(valid_nums_p1))
    print(sum(validate(str(n), p2=True) for n in valid_nums_p1))
