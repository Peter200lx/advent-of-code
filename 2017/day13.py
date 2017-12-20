DATA = """0: 3
1: 2
2: 4
4: 6
6: 4
8: 6
10: 5
12: 8
14: 8
16: 6
18: 8
20: 6
22: 10
24: 8
26: 12
28: 12
30: 8
32: 12
34: 8
36: 14
38: 12
40: 18
42: 12
44: 12
46: 9
48: 14
50: 18
52: 10
54: 14
56: 12
58: 12
60: 14
64: 14
68: 12
70: 17
72: 14
74: 12
76: 14
78: 14
82: 14
84: 14
94: 14
96: 14"""
EXAMPLE_DATA = """0: 3
1: 2
4: 4
6: 4"""


class FirewallLayer(object):

    def __init__(self, index, depth):
        self.index = index
        self.depth = depth
        if not self.depth:
            self.depth = None

    def found(self, timestamp):
        if self.depth is None:
            return None
        elif ((timestamp + self.index) % ((self.depth - 1) * 2)) == 0:
            return self.index, self.depth
        else:
            return None

    def __repr__(self):
        return f"FirewallLayer(index={self.index}, depth={self.depth})"


def build_firewall(recorded: str):
    ret_list = []
    for line in recorded.split('\n'):
        info = line.split(': ')
        ret_list.append(FirewallLayer(index=int(info[0]), depth=int(info[1])))
    return ret_list


def run_through_firewall(firewall, delay=0, fail_early=False):
    found = []
    for wall in firewall:
        wall_found = wall.found(delay)
        if wall_found:
            if fail_early:
                return True
            found.append(wall_found)
    if found:
        return sum(t[0] * t[1] for t in found)
    else:
        return None


def find_clean_run(firewall):
    caught = True
    i = 0
    while caught is not None:
        caught = run_through_firewall(firewall, i, fail_early=True)
        # if caught is None:
        #     print(f"Not caught with delay {i}")
        # else:
        #     print(f"caught score {caught} on run with delay {i}")
        i += 1
    return i - 1


if __name__ == '__main__':
    firewall = build_firewall(DATA)
    print(firewall)
    print(run_through_firewall(firewall))
    print(find_clean_run(firewall))
