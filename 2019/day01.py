from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


def fuel_calc(num):
    fuel = (num // 3) - 2
    return fuel if fuel > 0 else 0


def calc(list_o_mass):
    sum1 = sum2 = 0
    for num in list_o_mass:
        fuel_add = fuel_calc(num)
        sum1 += fuel_add
        sum2 += fuel_add
        while fuel_add:
            fuel_add = fuel_calc(fuel_add)
            sum2 += fuel_add
    return sum1, sum2


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    int_list = [int(i) for i in DATA.split("\n")]

    print(calc(int_list))
