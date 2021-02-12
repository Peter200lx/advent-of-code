import re
from collections import Counter
from pathlib import Path

FILE_DIR = Path(__file__).parent

example_data = """aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]"""


def calc_checksum(name: str) -> str:
    char_count = Counter(name)
    del char_count["-"]
    return "".join(sorted(sorted(char_count), key=lambda x: char_count[x], reverse=True)[:5])


def c_cipher(char, num):
    if char == "-":
        return " "
    norm = ord(char) - ord("a")
    return chr(ord("a") + (norm + num) % 26)


if __name__ == "__main__":
    DATA = (FILE_DIR / "day04.input").read_text().strip()

    val_list = []

    regex = re.compile(r"([a-z-]*)-([0-9]*)\[([a-z]*)\]")
    for row in DATA.split("\n"):
        results = regex.findall(row)
        name = results[0][0]
        num = int(results[0][1])
        checksum = results[0][2]
        char_count = Counter(name)
        mychecksum = calc_checksum(name)
        if checksum == mychecksum:
            val_list.append([name, num, checksum])

    val_sum = 0

    for valid in val_list:
        val_sum += valid[1]

    print(val_sum)

    for valid in val_list:
        name = "".join((c_cipher(c, valid[1]) for c in valid[0]))
        if "north" in name:
            print(f"{name} -> {valid[1]}")
