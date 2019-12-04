from collections import Counter


def validate(code):
    if len(code) != 6:
        return False
    prev = 0
    adjacent = False
    for char in code:
        cur = int(char)
        if cur == prev:
            adjacent = True
        if cur < prev:
            return False
        prev = cur
    return adjacent


def vp2(code):
    if len(code) != 6:
        return False
    c = Counter(code)
    prev = 0
    for char in code:
        cur = int(char)
        if cur < prev:
            return False
        prev = cur
    return any(v == 2 for k, v in c.items())


if __name__ == "__main__":
    DATA = "372037-905157"
    str_list = [int(num) for num in DATA.split("-")]
    count = 0
    cp2 = 0
    for i in range(str_list[0], str_list[1] + 1):
        if validate(str(i)):
            count += 1
        if vp2(str(i)):
            cp2 += 1

    print(count, cp2)
