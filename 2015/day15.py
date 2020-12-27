import re
from math import prod
from typing import NamedTuple, Iterator, Tuple, List

RE_NUMS = re.compile(r"-?\d+")

DATA = """Sprinkles: capacity 2, durability 0, flavor -2, texture 0, calories 3
Butterscotch: capacity 0, durability 5, flavor -3, texture 0, calories 3
Chocolate: capacity 0, durability 0, flavor 5, texture -1, calories 8
Candy: capacity 0, durability -1, flavor 0, texture 5, calories 8"""


class Cookie(NamedTuple):
    name: str
    cap: int
    dur: int
    flav: int
    tex: int
    cal: int

    def per_amount(self, amount: int) -> Tuple[int, int, int, int]:
        return self.cap * amount, self.dur * amount, self.flav * amount, self.tex * amount


def parse_input(input_str: str):
    cookies = []
    for line in input_str.split("\n"):
        name, _ = line.split(":")
        cookies.append(Cookie(name, *map(int, RE_NUMS.findall(line))))
    return cookies


def gen_combs(num_cookes: int, num_ing: int = 100) -> Iterator[Tuple[int, ...]]:
    assert num_cookes == 4, "Below code only works for 4 cookies"
    # I tried building this using permutations(range(num_ing+1),num_cookies-1) but that took > 4X longer
    for s in range(num_ing + 1):
        for b in range(num_ing + 1 - s):
            for ch in range(num_ing + 1 - s - b):
                yield s, b, ch, num_ing - s - b - ch


def find_best(cookies: List[Cookie]) -> Tuple[int, int]:
    best = 0
    best_at_500 = 0
    for cookie_quantities in gen_combs(len(cookies)):
        per_cookie_attrs = [c.per_amount(cookie_quantities[i]) for i, c in enumerate(cookies)]
        attrs_across_cookies = zip(*per_cookie_attrs)
        attr_totals = [sum(attr) for attr in attrs_across_cookies]
        if any(attr <= 0 for attr in attr_totals):
            continue
        total = prod(attr_totals)
        best = max(total, best)
        if sum(c.cal * cookie_quantities[i] for i, c in enumerate(cookies)) == 500:
            best_at_500 = max(total, best_at_500)
    return best, best_at_500


if __name__ == "__main__":
    COOKIES = parse_input(DATA)
    part_1, part_2 = find_best(COOKIES)
    print(part_1)
    print(part_2)
