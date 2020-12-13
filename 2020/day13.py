import math
from typing import NamedTuple, List

DATA = """1002576
13,x,x,x,x,x,x,37,x,x,x,x,x,449,x,29,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,19,x,x,x,23,x,x,x,x,x,x,x,773,x,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,17"""

VERY_LARGE_NUMBER = int(9e99)


class BusInfo(NamedTuple):
    id: int
    offset: int

    def valid_ts(self, t: int):
        return (t + self.offset) % self.id == 0

    def gen_ts(self):
        for i in range(VERY_LARGE_NUMBER):
            yield (i * self.id) - self.offset


def part_1(buses: List[BusInfo], earliest_time) -> int:
    min_next = VERY_LARGE_NUMBER, BusInfo(-1, -1)
    for bus in buses:
        bus_min = next(i * bus.id for i in range(VERY_LARGE_NUMBER) if i * bus.id > earliest_time)
        min_next = min(min_next, (bus_min, bus))
    time, bus = min_next
    return (time - earliest_time) * bus.id


def find_timestamp(buses: List[BusInfo]) -> int:
    timestamp = 0
    step = buses[0].id
    for bus in buses:
        while not bus.valid_ts(timestamp):
            timestamp += step
        step = (step * bus.id) // math.gcd(step, bus.id)
    return timestamp


def find_timestamp_brute(buses: List[BusInfo]) -> int:
    *driven_buses, driving_bus = sorted(buses)
    print(driving_bus)
    print(driven_buses)
    for ts in driving_bus.gen_ts():
        if all(b.valid_ts(ts) for b in driven_buses):
            return ts


if __name__ == "__main__":
    NUMBER, SEQUENCE = DATA.split("\n")
    NUMBER = int(NUMBER)
    BUSES = [BusInfo(int(val), i) for i, val in enumerate(SEQUENCE.split(",")) if val != "x"]
    print(part_1(BUSES, NUMBER))
    print(find_timestamp(BUSES))
