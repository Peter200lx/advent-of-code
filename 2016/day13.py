import heapq


def calc_space(x, y):
    n = x * x + 3 * x + 2 * x * y + y + y * y
    n += FAV_NUM
    return bin(n).count("1") % 2 == 0


def print_map(building):
    maxx = max(x for x, y in building)
    maxy = max(y for x, y in building)
    for y in range(maxy):
        line = ""
        for x in range(maxx):
            if (x, y) == DESTINATION:
                line += "D"
            elif (x, y) == START:
                line += "S"
            elif (x, y) not in building:
                line += "`"
            else:
                line += "." if building[x, y] else "#"
        print(line)


def find_possible(building, loc):
    next_moves = []
    for new_point in ((loc[0] + d[0], loc[1] + d[1]) for d in ((-1, 0), (1, 0), (0, -1), (0, 1))):
        if new_point[0] < 0 or new_point[1] < 0:
            continue
        if new_point in building:
            continue
        is_open = calc_space(*new_point)
        building[new_point] = is_open
        if is_open:
            next_moves.append(new_point)
    return next_moves


def calc_path(dest):
    prio_moves = []
    building = {START: True}
    heapq.heappush(prio_moves, (0, START))
    part_1 = part_2 = False
    while not (part_1 and part_2):
        steps, loc = heapq.heappop(prio_moves)
        if loc == dest:
            print_map(building)
            print(f"Part 1 took {steps} steps")
            part_1 = True
        if not part_2 and steps == PART_2_MAX:
            print_map(building)
            print(f"Part 2 saw {sum(building.values())} open spots in at most {PART_2_MAX} steps")
            part_2 = True
        for next_loc in find_possible(building, loc):
            heapq.heappush(prio_moves, (steps + 1, next_loc))


if __name__ == "__main__":
    START = (1, 1)
    DESTINATION = (31, 39)
    DATA = "1352"
    FAV_NUM = int(DATA)
    PART_2_MAX = 50
    calc_path(DESTINATION)
