from pathlib import Path


def fuel_calc(num):
    fuel = (num // 3) - 2
    if fuel < 0:
        return 0
    return fuel


def calc(start, list_o_cal):
    for i, num in enumerate(list_o_cal):
        list_o_cal[i] = (num // 3) - 2
    return sum(list_o_cal)


def calc_v2(start, list_o_cal):
    for i, num in enumerate(list_o_cal):
        list_o_cal[i] = (num // 3) - 2
        fuel_add = fuel_calc(num)
        while fuel_add:
            fuel_add = fuel_calc(fuel_add)
            list_o_cal[i] += fuel_add
    return sum(list_o_cal)


if __name__ == "__main__":
    DATA = Path("day01.input").read_text().strip()

    int_list = [int(i) for i in DATA.split("\n")]
    print(calc(0, int_list[:]))
    print(calc_v2(0, int_list[:]))
