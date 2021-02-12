from collections import Counter
from pathlib import Path

FILE_DIR = Path(__file__).parent

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
    DATA = (FILE_DIR / "day06.input").read_text().strip()
    TRANSMISSION = [l for l in DATA.split("\n")]

    counters = [Counter() for _ in range(len(TRANSMISSION[0]))]

    for attempt in TRANSMISSION:
        for i in range(len(counters)):
            counters[i].update(attempt[i])

    message = (c.most_common(1)[0][0] for c in counters)

    print("".join(message))

    message = (c.most_common()[-1][0] for c in counters)

    print("".join(message))
