def solve(numbers, find):
    last_spoken_time = {n: i + 1 for i, n in enumerate(numbers[:-1])}
    last_num = numbers[-1]
    for i in range(len(numbers), find):
        if last_num not in last_spoken_time:
            next_num = 0
        else:
            next_num = i - last_spoken_time[last_num]
        last_spoken_time[last_num] = i
        last_num = next_num
    return last_num


if __name__ == "__main__":
    DATA = """16,12,1,0,15,7,11"""
    NUMBER = [int(i) for i in DATA.split(",")]

    print(solve(NUMBER, 2020))
    print(solve(NUMBER, 30000000))
