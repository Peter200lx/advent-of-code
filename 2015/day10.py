DATA = """3113322113"""


def next_seq(input_str: str) -> str:
    last = input_str[0]
    count = 0
    result = []
    for c in input_str:
        if last == c:
            count += 1
        else:
            result.append(f"{count}{last}")
            last = c
            count = 1
    if last is not None:
        result.append(f"{count}{last}")
    return "".join(result)


def run_loop(start: str, n: int):
    current = start
    for _ in range(n):
        current = next_seq(current)
    return current


if __name__ == "__main__":
    assert next_seq("111221") == "312211"
    part_1 = run_loop(DATA, 40)
    print(len(part_1))
    print(len(run_loop(part_1, 10)))
