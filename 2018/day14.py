
DATA = """637061"""
SEED = [3, 7]


def part_1(start_list, after, final=10):
    cur_list = start_list[:]
    elfs = [0, 1]
    while len(cur_list) < after + final:
        elf_recipes = [cur_list[i] for i in elfs]
        new_recipes = [int(c) for c in str(sum(elf_recipes))]
        cur_list.extend(new_recipes)
        for i, elf in enumerate(elfs):
            elfs[i] = (elf + elf_recipes[i] + 1) % len(cur_list)

    return cur_list[after: after + final]


def part_2(start_list, compare_list):
    cur_list = start_list[:]
    elfs = [0, 1]
    while True:
        elf_recipes = [cur_list[i] for i in elfs]
        new_recipes = [int(c) for c in str(sum(elf_recipes))]
        for recipe in new_recipes:
            cur_list.append(recipe)
            if compare_list == cur_list[-len(compare_list):]:
                return len(cur_list) - len(compare_list)
        for i, elf in enumerate(elfs):
            elfs[i] = (elf + elf_recipes[i] + 1) % len(cur_list)


if __name__ == '__main__':
    my_list = part_1(SEED, int(DATA))
    print("".join(str(i) for i in my_list))
    print(part_2(SEED, list(int(c) for c in DATA)))
