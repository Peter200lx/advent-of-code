import re
from pathlib import Path

FILEDIR = Path(__file__).parent

example_data = """abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn"""


if __name__ == "__main__":
    DATA = (FILEDIR / "day07.input").read_text().strip()
    addresses = [l for l in DATA.split("\n")]

    hypernet = re.compile(r"\[([a-zA-Z]*)\]")
    abba = re.compile(r"([a-zA-Z])((?!\1)[a-zA-Z])\2\1")

    count = 0
    for addr in addresses:
        if abba.search(addr):
            possible = True
            for hn_part in hypernet.findall(addr):
                if abba.search(hn_part):
                    possible = False
            if possible:
                count += 1

    print(count)

    example_data = """aba[bab]xyz
    xyx[xyx]xyx
    aaa[kek]eke
    zazbz[bzb]cdb"""
    addresses = [l for l in DATA.split("\n")]
    aba = re.compile(r"(?=([a-zA-Z])((?!\1)[a-zA-Z])\1)")

    ssl_count = 0
    for addr in addresses:
        hypernet_parts = hypernet.findall(addr)
        # print(hypernet_parts)
        reg_parts = "".join((re.sub("|".join(hypernet_parts), "", addr)))
        # print(reg_parts)
        found = False
        for aba_part in aba.findall(reg_parts):
            # print(f"aba == {aba_part}")
            for ht_sec in hypernet_parts:
                if (aba_part[1] + aba_part[0] + aba_part[1]) in ht_sec:
                    found = True
                    break
            if found:
                break
        if found:
            # print('--FOUND!')
            ssl_count += 1

    print(ssl_count)
