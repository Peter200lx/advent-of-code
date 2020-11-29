import hashlib
import re

three_pair = re.compile(r"([a-z0-9])\1\1")
five_pair = re.compile(r"([a-z0-9])\1{4}")


def interesting_hash(key_hash):
    threes = set()
    fives = set()
    for match3 in three_pair.finditer(key_hash):
        c = match3.group(1)
        threes.add(c)
        break  # Missed only the first triplet applies initially
    if threes:
        for match5 in five_pair.finditer(key_hash):
            c = match5.group(1)
            fives.add(c)
    return threes, fives


def gen_keys(salt, stretches=0):
    valid_keys = []
    interesting_keys = {}
    for i in range(999_999_999):
        if len(valid_keys) >= 64:
            return valid_keys[-1][0]
        key_hash = hashlib.md5(f"{salt}{i}".encode()).hexdigest()
        for _ in range(stretches):
            key_hash = hashlib.md5(key_hash.encode()).hexdigest()
        threes, fives = interesting_hash(key_hash)
        if threes:
            interesting_keys[i] = (threes, fives, key_hash)
        check_i = i - 1001
        if check_i in interesting_keys:
            for j in range(check_i + 1, i + 1):
                if j in interesting_keys:
                    if interesting_keys[check_i][0] & interesting_keys[j][1]:
                        valid_keys.append((check_i, interesting_keys[check_i][2]))
                        break


if __name__ == "__main__":
    DATA = "jlmsuwbz"
    print(gen_keys(DATA))
    PART2_STRETCHES = 2016
    print(gen_keys(DATA, stretches=PART2_STRETCHES))
