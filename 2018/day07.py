DATA = """Step W must be finished before step B can begin.
Step G must be finished before step T can begin.
Step B must be finished before step P can begin.
Step R must be finished before step M can begin.
Step K must be finished before step Q can begin.
Step Z must be finished before step X can begin.
Step V must be finished before step S can begin.
Step D must be finished before step U can begin.
Step Y must be finished before step J can begin.
Step A must be finished before step C can begin.
Step M must be finished before step U can begin.
Step E must be finished before step X can begin.
Step T must be finished before step F can begin.
Step U must be finished before step C can begin.
Step C must be finished before step Q can begin.
Step S must be finished before step N can begin.
Step X must be finished before step H can begin.
Step F must be finished before step L can begin.
Step Q must be finished before step J can begin.
Step P must be finished before step J can begin.
Step I must be finished before step L can begin.
Step J must be finished before step L can begin.
Step L must be finished before step N can begin.
Step H must be finished before step O can begin.
Step N must be finished before step O can begin.
Step B must be finished before step S can begin.
Step A must be finished before step T can begin.
Step G must be finished before step K can begin.
Step Z must be finished before step N can begin.
Step V must be finished before step I can begin.
Step Z must be finished before step Q can begin.
Step I must be finished before step J can begin.
Step S must be finished before step I can begin.
Step P must be finished before step I can begin.
Step B must be finished before step C can begin.
Step M must be finished before step L can begin.
Step G must be finished before step Z can begin.
Step M must be finished before step C can begin.
Step U must be finished before step F can begin.
Step B must be finished before step Y can begin.
Step W must be finished before step U can begin.
Step G must be finished before step M can begin.
Step M must be finished before step J can begin.
Step C must be finished before step L can begin.
Step K must be finished before step D can begin.
Step S must be finished before step X can begin.
Step Q must be finished before step N can begin.
Step V must be finished before step N can begin.
Step R must be finished before step C can begin.
Step E must be finished before step H can begin.
Step D must be finished before step P can begin.
Step H must be finished before step N can begin.
Step X must be finished before step O can begin.
Step K must be finished before step Y can begin.
Step R must be finished before step F can begin.
Step L must be finished before step O can begin.
Step Y must be finished before step M can begin.
Step T must be finished before step I can begin.
Step T must be finished before step Q can begin.
Step B must be finished before step F can begin.
Step C must be finished before step N can begin.
Step V must be finished before step M can begin.
Step T must be finished before step N can begin.
Step S must be finished before step L can begin.
Step P must be finished before step H can begin.
Step X must be finished before step Q can begin.
Step Z must be finished before step I can begin.
Step Q must be finished before step O can begin.
Step I must be finished before step N can begin.
Step E must be finished before step P can begin.
Step R must be finished before step L can begin.
Step P must be finished before step L can begin.
Step T must be finished before step H can begin.
Step G must be finished before step X can begin.
Step J must be finished before step H can begin.
Step G must be finished before step V can begin.
Step K must be finished before step N can begin.
Step R must be finished before step Q can begin.
Step Z must be finished before step T can begin.
Step E must be finished before step F can begin.
Step Y must be finished before step H can begin.
Step P must be finished before step N can begin.
Step S must be finished before step O can begin.
Step L must be finished before step H can begin.
Step W must be finished before step E can begin.
Step X must be finished before step N can begin.
Step Z must be finished before step D can begin.
Step A must be finished before step H can begin.
Step T must be finished before step X can begin.
Step E must be finished before step Q can begin.
Step K must be finished before step U can begin.
Step M must be finished before step T can begin.
Step J must be finished before step O can begin.
Step D must be finished before step N can begin.
Step K must be finished before step A can begin.
Step G must be finished before step E can begin.
Step R must be finished before step H can begin.
Step W must be finished before step M can begin.
Step U must be finished before step N can begin.
Step Q must be finished before step H can begin.
Step Y must be finished before step A can begin.""".split('\n')

EXAMPLE_DATA = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""".split('\n')

BASE_WAIT_TIME = 60
MAX_WORKERS = 5


class Node:
    def __init__(self, value):
        self.value = value
        self.blocked_by = set()
        self.blocking = []
        self.ticks_left = BASE_WAIT_TIME + (ord(value) - ord("A") + 1)

    def can_add(self, str_so_far):
        for c in self.blocked_by:
            if c not in str_so_far:
                return False
        return True

    def valid_nodes(self, str_so_far):
        return [n for n in self.blocking if n.can_add(str_so_far)]

    def tick_and_done(self):
        self.ticks_left -= 1
        return not self.ticks_left

    def __repr__(self):
        return f"Node({self.value}, {self.blocking}, {''.join(self.blocked_by)})"

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value


def build_graph(instructions):
    parent_dict = {}
    for inst in instructions:
        parts = inst.split()
        if parts[1] not in parent_dict:
            parent_dict[parts[1]] = Node(parts[1])
        if parts[7] not in parent_dict:
            parent_dict[parts[7]] = Node(parts[7])
        parent_dict[parts[1]].blocking.append(parent_dict[parts[7]])
        parent_dict[parts[7]].blocked_by.add(parts[1])
    # print([(key, ''.join(parent_dict[key].blocked_by)) for key in parent_dict.keys()])
    starting_list = []
    for key in parent_dict:
        if not parent_dict[key].blocked_by:
            starting_list.append(parent_dict[key])
    return starting_list


def part_1(start_list):
    possible_list = start_list[:]
    ret_str = ""
    while possible_list:
        possible_list.sort()
        node = possible_list.pop(0)
        ret_str += node.value
        possible_list.extend(node.valid_nodes(ret_str))
    return ret_str


def part_2(start_list):
    possible_list = start_list[:]
    ret_str = ""
    tick = 0
    workers = []
    while possible_list or workers:
        possible_list.sort()
        while possible_list and len(workers) < MAX_WORKERS:
            workers.append(possible_list.pop(0))
        to_del = []
        for i, node in enumerate(workers):
            if node.tick_and_done():
                ret_str += node.value
                possible_list.extend(node.valid_nodes(ret_str))
                to_del.append(i)
        for i in sorted(to_del, reverse=True):
            del workers[i]
        tick += 1
    return ret_str, tick


if __name__ == '__main__':
    starting = build_graph(DATA)
    # print(starting)
    print(part_1(starting))
    # GKRVWBESYAMZDPTIUCFXQJLHNO
    print(part_2(starting))
