from collections import Counter
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

example_data = """eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar"""

if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    TRANSMISSION = [l for l in DATA.split("\n")]

    counters = [Counter() for _ in range(len(TRANSMISSION[0]))]

    for attempt in TRANSMISSION:
        for i in range(len(counters)):
            counters[i].update(attempt[i])

    message = (c.most_common(1)[0][0] for c in counters)

    print("".join(message))

    message = (c.most_common()[-1][0] for c in counters)

    print("".join(message))
