from pathlib import Path

if __name__ == "__main__":
    DATA = Path("day01.input").read_text().strip()
    INSTRUCTIONS = [(i.strip()[0], int(i.strip()[1:])) for i in DATA.split(",")]

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
    for inst in INSTRUCTIONS:
        cur_dir = turn_map[cur_dir][inst[0]]
        dir_inst = value_map[cur_dir]
        count[dir_inst[0]] += dir_inst[1] * inst[1]

    print(str(abs(count["ns"]) + abs(count["ew"])))

    loc_map = set("0,0")
    cur_loc = {"ns": 0, "ew": 0}
    found = False

    for inst in INSTRUCTIONS:
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
