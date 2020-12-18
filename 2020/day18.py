import re
from operator import mul, add
from pathlib import Path
from typing import Callable, Optional

FILE_DIR = Path(__file__).parent


def seq_eval(chunk: str):
    i = 0
    n = None
    op: Optional[Callable[[int, int], int]] = None
    while i < len(chunk):
        if chunk[i] == "(":
            sub_i, sub_n = seq_eval(chunk[i + 1 :])
            i += sub_i
            if n is None:
                n = sub_n
            else:
                assert op is not None
                n = op(n, sub_n)
        elif chunk[i] == ")":
            return i + 1, n
        elif chunk[i].isdigit():
            if n is None:
                assert op is None
                n = int(chunk[i])
            else:
                assert op is not None
                n = op(n, int(chunk[i]))
                op = None
        elif chunk[i] == "*":
            op = mul
        elif chunk[i] == "+":
            op = add
        else:
            raise Exception(f"Unexpected character {chunk[i]}")
        i += 1
    return i, n


def part_1(lines):
    expressions = [seq_eval(line.replace(" ", "")) for line in lines.split("\n")]
    return [t[1] for t in expressions]


def plus_prio_eval(chunk: str, mul_calc=False):
    print(f"chunk: {chunk}")
    i = 0
    n = None
    op: Optional[Callable[[int, int], int]] = None
    while i < len(chunk):
        print(chunk, n)
        print(" " * i + "^")
        if chunk[i] == "(":
            sub_i, sub_n = plus_prio_eval(chunk[i + 1 :])
            i += sub_i
            if n is None:
                n = sub_n
            else:
                assert op is not None
                n = op(n, sub_n)
                op = None
            if mul_calc:
                print(f"Escaping mul with {n} having consumed {chunk[:i + 1]}")
                return i + 1, n
        elif chunk[i] == ")":
            print(f"Going up with {n} having consumed {chunk[:i + 1]}")
            return i + 1, n
        elif chunk[i].isdigit():
            if n is None:
                assert op is None
                n = int(chunk[i])
            else:
                assert op is not None
                n = op(n, int(chunk[i]))
                op = None
        elif chunk[i] == "*":
            sub_i, sub_n = plus_prio_eval(chunk[i + 1 :], mul_calc=True)
            n *= sub_n
            i += sub_i
            if mul_calc:
                print(f"Escaping mul with {n} having consumed {chunk[:i + 1]}")
                return i + 1, n
        elif chunk[i] == "+":
            op = add
        else:
            raise Exception(f"Unexpected character {chunk[i]}")
        i += 1
    print(f"Returning with {n} having consumed {chunk[: i]}")
    return i, n


SOLO_PAREN = re.compile(r"\(([^()]+)\)")
NUM_PLUS_NUM = re.compile(r"(\d+)\+(\d+)")
NUM_MUL_NUM = re.compile(r"(\d+)\*(\d+)")


def regex_sum(match: re.Match):
    return f"{int(match.group(1)) + int(match.group(2))}"


def regex_mul(match: re.Match):
    return f"{int(match.group(1)) * int(match.group(2))}"


def run_calc(chunk: str):
    chunk = NUM_PLUS_NUM.sub(regex_sum, chunk)
    chunk = NUM_PLUS_NUM.sub(regex_sum, chunk)
    chunk = NUM_PLUS_NUM.sub(regex_sum, chunk)
    chunk = NUM_MUL_NUM.sub(regex_mul, chunk)
    chunk = NUM_MUL_NUM.sub(regex_mul, chunk)
    chunk = NUM_MUL_NUM.sub(regex_mul, chunk)
    return chunk


def regex_parse(match: re.Match):
    return run_calc(match.group(1))


def regex_eval(chunk: str):
    new_chunk = SOLO_PAREN.sub(regex_parse, chunk)
    while new_chunk != chunk:
        new_chunk, chunk = SOLO_PAREN.sub(regex_parse, new_chunk), new_chunk
    return int(run_calc(chunk))


def part_2(lines):
    return [regex_eval(s.replace(" ", "")) for s in lines.split("\n")]
    # expressions = [plus_prio_eval(line.replace(" ", "")) for line in lines.split("\n")]
    # print("Finally")
    # return [t[1] for t in expressions]


if __name__ == "__main__":
    DATA = (FILE_DIR / "day18.input").read_text().strip()
    assert sum(part_1("1 + (2 * 3) + (4 * (5 + 6))")) == 51
    assert sum(part_1("2 * 3 + (4 * 5)")) == 26
    assert sum(part_1("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")) == 12240
    assert sum(part_1("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")) == 13632
    print(sum(part_1(DATA)))

    assert sum(part_2("1 + (2 * 3) + (4 * (5 + 6))")) == 51
    assert sum(part_2("2 * 3 + (4 * 5)")) == 46
    assert sum(part_2("5 + (8 * 3 + 9 + 3 * 4 * 3)")) == 1445
    assert sum(part_2("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")) == 669060
    assert sum(part_2("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")) == 23340
    assert sum(part_2("(5 * 3 * 6) + 4")) == 94
    assert sum(part_2("6 + (3 * 1) * 3")) == 27
    assert sum(part_2("8 * 9 + (6 + 3 * 3 + 9 + 4) * 2 + ((5 * 3 + 5 + 7 * 6) + 7) * 4")) == 2247264
    print(sum(part_2(DATA)))
