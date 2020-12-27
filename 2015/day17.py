from itertools import combinations

DATA = """33
14
18
20
45
35
16
35
1
13
18
13
50
44
48
6
24
41
30
42"""


if __name__ == "__main__":
    CONTAINERS = [int(line) for line in DATA.split("\n")]
    print(sum(sum(comb) == 150 for i in range(len(CONTAINERS)) for comb in combinations(CONTAINERS, i)))
    min_containers = next(i for i in range(len(CONTAINERS)) for comb in combinations(CONTAINERS, i) if sum(comb) == 150)
    print(sum(sum(comb) == 150 for comb in combinations(CONTAINERS, min_containers)))
