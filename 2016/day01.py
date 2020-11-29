from enum import Enum

data = "R4, R3, R5, L3, L5, R2, L2, R5, L2, R5, R5, R5, R1, R3, L2, L2, L1, R5, L3, R1, L2, R1, L3, L5, L1, R3, L4, R2, R4, L3, L1, R4, L4, R3, L5, L3, R188, R4, L1, R48, L5, R4, R71, R3, L2, R188, L3, R2, L3, R3, L5, L1, R1, L2, L4, L2, R5, L3, R3, R3, R4, L3, L4, R5, L4, L4, R3, R4, L4, R1, L3, L1, L1, R4, R1, L4, R1, L1, L3, R2, L2, R2, L1, R5, R3, R4, L5, R2, R5, L5, R1, R2, L1, L3, R3, R1, R3, L4, R4, L4, L1, R1, L2, L2, L4, R1, L3, R4, L2, R3, L1, L5, R4, R5, R2, R5, R1, R5, R1, R3, L3, L2, L2, L5, R2, L2, R5, R5, L2, R3, L5, R5, L2, R4, R2, L1, R3, L5, R3, R2, R5, L1, R3, L2, R2, R1"

instructions = [(i.strip()[0], int(i.strip()[1:])) for i in data.split(",")]

count = {"ns": 0, "ew": 0}

turn_map = {
    "North": {"L": "West", "R": "East"},
    "South": {"L": "East", "R": "West"},
    "East": {"L": "North", "R": "South"},
    "West": {"L": "South", "R": "North"},
}
value_map = {
    "North": ("ns", 1),
    "South": ("ns", -1),
    "East": ("ew", 1),
    "West": ("ew", -1),
}

cur_dir = "North"
for inst in instructions:
    cur_dir = turn_map[cur_dir][inst[0]]
    dir_inst = value_map[cur_dir]
    count[dir_inst[0]] += dir_inst[1] * inst[1]

print(str(abs(count["ns"]) + abs(count["ew"])))


loc_map = set("0,0")
cur_loc = {"ns": 0, "ew": 0}
found = False

for inst in instructions:
    cur_dir = turn_map[cur_dir][inst[0]]
    dir_inst = value_map[cur_dir]
    for movement in range(inst[1]):
        cur_loc[dir_inst[0]] += dir_inst[1]
        cur_loc_str = f"{cur_loc['ns']},{cur_loc['ew']}"
        # print(f"{inst} gave {cur_loc_str}")
        if cur_loc_str not in loc_map:
            loc_map.add(cur_loc_str)
        else:
            found = True
            break
    if found:
        break

print(str(abs(cur_loc["ns"]) + abs(cur_loc["ew"])))
