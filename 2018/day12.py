
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
FULL_RANGE = range(-3, 232)


def parse_input(input_list):
    row = {i for i, c in enumerate(input_list[0][15:]) if c == "#"}
    transforms = {}
    for input_str in input_list[2:]:
        before, after = input_str.split(" => ")
        transforms[before] = after
    return row, transforms


def run_transform(row, transforms):
    bottom = min(row)
    top = max(row)
    new_set = set()
    for i in range(bottom - 3, top + 4):
        check = "".join("#" if j in row else "." for j in range(i - 2, i + 3))
        if transforms.get(check) == "#":
            new_set.add(i)
    return new_set


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
    # print("".join(["#" if i in plants else " " for i in FULL_RANGE]))
    x_iters = []
    y_sums = []
    for iteration in range(1, 21):
        plants = run_transform(plants, instructions)
        # print("".join(["#" if i in plants else " " for i in FULL_RANGE]))
        if iteration > 17:  # Prime the pump for part 2
            x_iters.append(iteration)
            y_sums.append(sum([i for i in plants]))
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
        # print("".join(["#" if i in plants else " " for i in FULL_RANGE]))
        x_iters.append(iteration)
        y_sums.append(sum([i for i in plants]))
