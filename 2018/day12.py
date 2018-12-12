
DATA = """initial state: ##.#.####..#####..#.....##....#.#######..#.#...........#......##...##.#...####..##.#..##.....#..####

#..#. => #
.###. => .
..##. => .
....# => .
#...# => .
.#.#. => .
#.#.# => #
#.... => .
#.#.. => #
###.# => .
.#... => #
#.### => .
.#.## => #
..#.. => #
.#### => .
..### => #
...#. => .
##.#. => #
##.## => #
.##.# => #
###.. => .
..#.# => .
...## => #
##... => #
##### => .
#.##. => .
.#..# => #
##..# => .
..... => .
####. => #
#..## => .
.##.. => #""".split('\n')

EXAMPLE_DATA = """initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #""".split('\n')


PART_2_ITER = 50000000000


def parse_input(input_list):
    row = {}
    i = 0
    for c in input_list[0]:
        if c not in (".", "#"):
            continue
        row[i] = (c == "#")
        i += 1
    transforms = {}
    for input_str in input_list[2:]:
        before, after = input_str.split(" => ")
        before = tuple(c == "#" for c in before)
        transforms[before] = (after == "#")
    return row, transforms


def run_transform(row, transforms):
    bottom = min(row.keys())
    top = max(row.keys())
    new_dict = {}
    for i in range(bottom - 3, top + 4):
        check = []
        for j in range(i - 2, i + 3):
            check.append(row.get(j, False))
        check = tuple(check)
        if check in transforms:
            new_dict[i] = transforms[check]
        elif bottom <= i <= top:
            new_dict[i] = False
    return new_dict


def straight_line(x_vals, y_vals):
    assert len(x_vals) == 3
    assert len(y_vals) == 3
    slope = (y_vals[1] - y_vals[0]) / (x_vals[1] - x_vals[0])
    slope2 = (y_vals[2] - y_vals[1]) / (x_vals[2] - x_vals[1])
    if slope != slope2:
        return False
    intercept = y_vals[0] - slope * x_vals[0]
    return slope, intercept


if __name__ == '__main__':
    plants, instructions = parse_input(DATA)
    x_iters = []
    y_sums = []
    for iteration in range(1, 21):
        plants = run_transform(plants, instructions)
        if iteration > 17:  # Prime the pump for part 2
            x_iters.append(iteration)
            y_sums.append(sum([i for i in plants if plants[i]]))
    print(f"Part 1: {y_sums[-1]}")

    for iteration in range(21, PART_2_ITER):
        line = straight_line(x_iters, y_sums)
        if line:
            part_2 = int(line[0] * PART_2_ITER + line[1])
            print(f"Part 2: {part_2}")
            break
        x_iters.pop(0)
        y_sums.pop(0)
        plants = run_transform(plants, instructions)
        x_iters.append(iteration)
        y_sums.append(sum([i for i in plants if plants[i]]))
