from hashlib import md5

DATA = """ckczppom"""
START_KEY_P1 = "00000"
START_KEY_P2 = "000000"


def valid_num(key: str, num: int, match: str) -> bool:
    input_data = (key + str(num)).encode()
    md5sum = md5(input_data).hexdigest()
    if not num % 100000:
        print(f'{key}{num} -> {md5sum}')
    if md5sum.startswith(match):
        print(f'{key}{num} -> {md5sum}')
        return True
    else:
        return False


def find_lowest_int(key: str, match: str) -> int:
    i = 0
    while not valid_num(key, i, match):
        i += 1
    return i


if __name__ == '__main__':
    print(find_lowest_int(DATA, START_KEY_P1))
    print(find_lowest_int(DATA, START_KEY_P2))