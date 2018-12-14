DATA = """637061"""
SEED = [3, 7]


def combined_solution(seed_list, input_str, final=10):
    after = int(input_str)
    compare_list = list(int(c) for c in input_str)
    cur_list = seed_list[:]
    elfs = list(range(len(seed_list)))
    part_1_found = False
    part_2_found = False
    while not (part_1_found and part_2_found):
        elf_recipes = [cur_list[i] for i in elfs]
        new_recipes = [int(c) for c in str(sum(elf_recipes))]
        for recipe in new_recipes:
            cur_list.append(recipe)

            if not part_2_found and compare_list == cur_list[-len(compare_list):]:
                print(f"Part 2: {len(cur_list) - len(compare_list)}")
                part_2_found = True

        for i in range(len(elfs)):
            elfs[i] += elf_recipes[i] + 1
            elfs[i] %= len(cur_list)

        if not part_1_found and len(cur_list) >= after + final:
            print(f"Part 1: {''.join(str(c) for c in cur_list[after:after + final])}")
            part_1_found = True


if __name__ == '__main__':
    combined_solution(SEED, DATA)
