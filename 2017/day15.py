from typing import Dict, Generator

FACTORS = {'A': 16807, 'B': 48271}
MOD_VAL = 2147483647
DATA = {'A': 634, 'B': 301}
"""Generator A starts with 634
Generator B starts with 301"""
EXAMPLE_DATA = {'A': 65, 'B': 8921}
"""Generator A starts with 65
Generator B starts with 8921"""
TOTAL_PAIRS1 = 40000000
TOTAL_PAIRS2 = 5000000
LOW_16_BITS = 0b1111111111111111
PART_2_MULT = {'A': 4, 'B': 8}


def mult_gen(factor: int, start_val: int, multiple: int = 1) -> Generator[int, None, None]:
    last_val = start_val % MOD_VAL
    while True:
        last_val *= factor
        last_val %= MOD_VAL
        if last_val % multiple == 0:
            yield last_val


def find_count(start_dict: Dict[str, int], run_to: int, p2_dict: Dict[str, int] = None) -> int:
    if p2_dict is None:
        p2_dict = {'A': 1, 'B': 1}
    gen_a = mult_gen(FACTORS['A'], start_dict['A'], p2_dict['A'])
    gen_b = mult_gen(FACTORS['B'], start_dict['B'], p2_dict['B'])
    count = 0
    for i in range(run_to):
        a_val = next(gen_a)
        b_val = next(gen_b)
        # print(f"gen A: {a_val:10} {a_val:038b}")
        # print(f"gen B: {b_val:10} {b_val:038b}")
        if a_val & LOW_16_BITS == b_val & LOW_16_BITS:
            # print(i)
            count += 1
    return count


if __name__ == '__main__':
    print(find_count(DATA, TOTAL_PAIRS1))
    print(find_count(DATA, TOTAL_PAIRS2, PART_2_MULT))
