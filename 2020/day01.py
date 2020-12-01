from itertools import permutations


if __name__ == "__main__":
    with open("day01.input", "r") as in_file:
        DATA = in_file.read().strip("\n")

    int_list = [int(i) for i in DATA.split("\n")]
    for x, y in permutations(int_list, 2):
        if x + y == 2020:
            print(x, y, x * y)
            break
    for x, y, z in permutations(int_list, 3):
        if x + y + z == 2020:
            print(x, y, z, z * x * y)
            break
