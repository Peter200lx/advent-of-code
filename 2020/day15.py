from typing import List

DATA = """16,12,1,0,15,7,11"""


def solve(numbers: List[int], find: int) -> int:
    last_spoken_time = {n: i for i, n in enumerate(numbers[:-1], start=1)}
    last_num = numbers[-1]
    for i in range(len(numbers), find):
        next_num = i - last_spoken_time.get(last_num, i)
        last_spoken_time[last_num] = i
        last_num = next_num
    return last_num


if __name__ == "__main__":
    NUMBERS = [int(i) for i in DATA.split(",")]

    print(solve(NUMBERS, 2020))
    print(solve(NUMBERS, 30000000))
