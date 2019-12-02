from pathlib import Path


def calc(list_o_codes, overrides):
    list_o_codes = list_o_codes[:]
    for loc, val in overrides:
        list_o_codes[loc] = val
    index = 0
    while list_o_codes[index] != 99:
        op, a, b, p = list_o_codes[index : index + 4]
        if op == 1:
            list_o_codes[p] = list_o_codes[a] + list_o_codes[b]
        elif op == 2:
            list_o_codes[p] = list_o_codes[a] * list_o_codes[b]
        else:
            raise ValueError(f"Bad op code {op}")
        index += 4
    return list_o_codes[0]


def find_state(list_o_codes, desired_state):
    for noun in range(100):
        for verb in range(100):
            if calc(list_o_codes, ((1, noun), (2, verb))) == desired_state:
                return noun, verb


if __name__ == "__main__":
    DATA = Path("day02.input").read_text().strip()
    int_list = [int(i) for i in DATA.split(",")]

    print(calc(int_list, ((1, 12), (2, 2))))
    n, v = find_state(int_list, 19690720)
    print(n, v, 100 * n + v)
