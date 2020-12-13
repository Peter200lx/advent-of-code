import math
from typing import NamedTuple

DATA = """1002576
13,x,x,x,x,x,x,37,x,x,x,x,x,449,x,29,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,19,x,x,x,23,x,x,x,x,x,x,x,773,x,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,17"""


class BusInfo(NamedTuple):
    id: int
    offset: int

    @property
    def mod(self):
        return self.id - self.offset

    def valid_ts(self, t: int):
        return (t + self.offset) % self.id == 0

    def gen_ts(self):
        for i in range(999999999999999999999):
            yield (i * self.id) - self.offset


def find_timestamp(raw_busses):
    busses = [BusInfo(val, i) for i, val in enumerate(raw_busses) if not isinstance(val, str)]
    timestamp = 0
    step = busses[0].id
    for bus in busses:
        while not bus.valid_ts(timestamp):
            timestamp += step
        if bus.valid_ts(timestamp):
            step = (step * bus.id) // math.gcd(step, bus.id)
    return timestamp


def find_timestamp_brute(buses):
    bus_data = [BusInfo(val, i) for i, val in enumerate(buses) if not isinstance(val, str)]
    bus_data.sort()
    *driven_buses, driving_bus = bus_data
    print(driving_bus)
    print(driven_buses)
    for ts in driving_bus.gen_ts():
        if all(b.valid_ts(ts) for b in driven_buses):
            return ts
    print(bus_data)


if __name__ == "__main__":
    NUMBER, SEQUENCE = DATA.split("\n")
    NUMBER = int(NUMBER)
    SEQUENCE = [int(x) if x != "x" else "x" for x in SEQUENCE.split(",")]
    print(NUMBER, SEQUENCE)
    min_next = 99999999999999999999999999999, None
    for n in SEQUENCE:
        if not isinstance(n, int):
            continue
        for i in range(999999999999999):
            if i * n > NUMBER:
                min_next = min(min_next, (i * n, n))
                break
    print(min_next)
    print((min_next[0] - NUMBER) * min_next[1])
    print(find_timestamp(SEQUENCE))
