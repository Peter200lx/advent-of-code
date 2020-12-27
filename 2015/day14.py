import re
from typing import NamedTuple, List

RE_NUMS = re.compile(r"-?\d+")

DATA = """Vixen can fly 19 km/s for 7 seconds, but then must rest for 124 seconds.
Rudolph can fly 3 km/s for 15 seconds, but then must rest for 28 seconds.
Donner can fly 19 km/s for 9 seconds, but then must rest for 164 seconds.
Blitzen can fly 19 km/s for 9 seconds, but then must rest for 158 seconds.
Comet can fly 13 km/s for 7 seconds, but then must rest for 82 seconds.
Cupid can fly 25 km/s for 6 seconds, but then must rest for 145 seconds.
Dasher can fly 14 km/s for 3 seconds, but then must rest for 38 seconds.
Dancer can fly 3 km/s for 16 seconds, but then must rest for 37 seconds.
Prancer can fly 25 km/s for 6 seconds, but then must rest for 143 seconds."""

DURATION = 2503


class Reindeer(NamedTuple):
    name: str
    speed: int
    flying: int
    resting: int


def parse_input(input_str: str):
    reindeers = []
    for line in input_str.split("\n"):
        name, *_ = line.split()
        speed, flying, resting = map(int, RE_NUMS.findall(line))
        reindeers.append(Reindeer(name, speed, flying, resting))
    return reindeers


def distance(reindeer: Reindeer, time: int):
    section = reindeer.flying + reindeer.resting
    full_sequences = time // section
    dist = full_sequences * reindeer.speed * reindeer.flying
    remaining_time = time % section
    if remaining_time > reindeer.flying:
        return dist + reindeer.speed * reindeer.flying
    else:
        return dist + reindeer.speed * remaining_time


def score_points(reindeers: List[Reindeer], time: int):
    score = {r: 0 for r in reindeers}
    for t in range(1, time + 1):
        t_dist = {r: distance(r, t) for r in reindeers}
        max_dist = max(t_dist.values())
        for reindeer, dist in t_dist.items():
            if dist != max_dist:
                continue
            score[reindeer] += 1
    return max(score.values())


if __name__ == "__main__":
    REINDEERS = parse_input(DATA)
    print(max(distance(r, DURATION) for r in REINDEERS))
    print(score_points(REINDEERS, DURATION))
