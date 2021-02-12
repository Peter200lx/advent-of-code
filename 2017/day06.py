example_data = """0 2   7   0"""
data = """4	10	4	1	8	4	9	14	5	1	14	15	0	15	3	5"""

banks = [int(i) for i in data.split()]

seen = {}


def distribute_from_index(buckets, index):
    pool = buckets[index]
    buckets[index] = 0
    while pool:
        index += 1
        index %= len(buckets)
        buckets[index] += 1
        pool -= 1


count = 0
while tuple(banks) not in seen:
    seen[tuple(banks)] = count
    distribute_from_index(banks, banks.index(max(banks)))
    count += 1

print(count)
print(count - seen[tuple(banks)])
