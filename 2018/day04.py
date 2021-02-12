import re
from collections import Counter, defaultdict
from pathlib import Path

FILE_DIR = Path(__file__).parent

re_log = re.compile(r".*\[([0-9-]+) (\d+):(\d+)[^0-9]*(Guard|falls|wakes).*")
re_gnum = re.compile(r".*#(\d+).*")


def build_asleep_dict(logs):
    cur_guard = -1
    asleep = None
    guards = defaultdict(list)
    for log in logs:
        match = re_log.match(log)
        _, _, minute, ltype = match.groups()
        if ltype == "Guard":
            assert not asleep
            cur_guard = int(re_gnum.match(log).group(1))
        elif ltype == "falls":
            assert not asleep
            asleep = int(minute)
        elif ltype == "wakes":
            assert asleep is not None
            guards[cur_guard].extend(range(asleep, int(minute)))
            asleep = None
    return guards


def part_1(guards):
    worst_guard = max(guards, key=lambda x: len(guards.get(x)))
    worst_time = Counter(guards[worst_guard]).most_common(1)[0][0]
    return worst_time * worst_guard


def part_2(guards):
    worst_guard = (0, 0, 0)
    for guard, minutes in guards.items():
        time, number = Counter(minutes).most_common(1)[0]
        if number > worst_guard[0]:
            worst_guard = (number, time, guard)
    return worst_guard[1] * worst_guard[2]


if __name__ == "__main__":
    DATA = (FILE_DIR / "day04.input").read_text().strip()

    guard_dict = build_asleep_dict(sorted(DATA.split("\n")))
    print(part_1(guard_dict))
    print(part_2(guard_dict))
