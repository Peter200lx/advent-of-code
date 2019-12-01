from pathlib import Path


def fuel_calc(num):
    fuel = (num // 3) - 2
    return fuel if fuel > 0 else 0


def calc(list_o_mass):
    for i, num in enumerate(list_o_mass):
        list_o_mass[i] = fuel_calc(num)
    return sum(list_o_mass)


def calc_v2(list_o_mass):
    for i, num in enumerate(list_o_mass):
        list_o_mass[i] = fuel_add = fuel_calc(num)
        while fuel_add:
            fuel_add = fuel_calc(fuel_add)
            list_o_mass[i] += fuel_add
    return sum(list_o_mass)


if __name__ == "__main__":
    DATA = Path("day01.input").read_text().strip()
    int_list = [int(i) for i in DATA.split("\n")]

    print(calc(int_list[:]))
    print(calc_v2(int_list[:]))
