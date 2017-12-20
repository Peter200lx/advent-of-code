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

    def __init__(self, depth):
        self.state = [False for _ in range(depth)]
        if self.state:
            self.state[0] = True
        self.direction = 1
        self.has_packet = False

    def enter(self):
        self.has_packet = True

    def exit(self):
        self.has_packet = False

    def step(self):
        if not self.state:
            return None
        index = self.state.index(True)
        self.state[index] = False
        if (index == 0 and self.direction == -1) or (index == len(self.state) - 1 and self.direction == 1):
            self.direction *= -1
        new_index = index + self.direction
        self.state[new_index] = True
        if index == 0 and self.has_packet:
            return len(self.state)
        else:
            return None

    def reset(self):
        if self.state:
            self.state = [False for _ in range(len(self.state))]
            self.state[0] = True
            self.direction = 1
            self.has_packet = False

    def __repr__(self):
        return f"FirewallLayer({''.join(('T' if d else 'F' for d in self.state))}, {self.direction}, {'Packet' if self.has_packet else 'Empty'})"


def build_firewall(recorded: str):
    ret_list = []
    for line in recorded.split('\n'):
        info = line.split(': ')
        layer, size = int(info[0]), int(info[1])
        if len(ret_list) < layer:
            for _ in range(len(ret_list), layer):
                ret_list.append(FirewallLayer(0))
        ret_list.append(FirewallLayer(size))
    return ret_list


def run_through_firewall(firewall, delay=0):
    if delay:
        [[w.step() for w in firewall] for _ in range(delay)]
    depth = 0
    found = []
    for wall in firewall:
        wall.enter()
        # print(firewall)
        wall_found = [(c, depth) for c in (w.step() for w in firewall) if c is not None]
        if wall_found:
            found.append(wall_found[0])
        wall.exit()
        depth += 1
    if found:
        return sum(t[0] * t[1] for t in found)
    else:
        return None


def find_clean_run(firewall):
    caught = False
    i = 0
    while caught is not None:
        [wall.reset() for wall in firewall]
        caught = run_through_firewall(firewall, i)
        if caught is None:
            print(f"Not caught with delay {i}")
        else:
            print(f"caught score {caught} on run with delay {i}")
        i += 1
    return i - 1


firewall = build_firewall(EXAMPLE_DATA)
print(firewall)
print(run_through_firewall(firewall))
print(find_clean_run(firewall))
