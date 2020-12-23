from typing import Dict, Optional, Tuple

DATA = """284573961"""
EXAMPLE_DATA = """389125467"""

P1_RUNS = 100
P2_TOTAL_CUPS = 1_000_000
P2_RUNS = 10_000_000


class Cup:
    def __init__(self, value: int, max_val: int, cup_cache: Dict[int, "Cup"]):
        self.next: Optional["Cup"] = None
        self.previous: Optional["Cup"] = None
        self.value = value
        self.max_val = max_val
        self.cup_cache = cup_cache

    def __repr__(self):
        return f"Cup({self.value}, p={self.previous and self.previous.value}, n={self.next and self.next.value})"

    @staticmethod
    def load_input(seq: str) -> "Cup":
        cup_cache = {}
        cur_cup = first_cup = Cup(int(seq[0]), 9, cup_cache)
        cup_cache[first_cup.value] = first_cup
        for c in seq[1:]:
            new_cup = Cup(int(c), 9, cup_cache)
            cup_cache[new_cup.value] = new_cup
            new_cup.previous = cur_cup
            cur_cup.next = new_cup
            cur_cup = new_cup
        first_cup.previous = cur_cup
        cur_cup.next = first_cup
        return first_cup

    @staticmethod
    def load_input_p2(seq: str) -> "Cup":
        cup_cache = {}
        cur_cup = first_cup = Cup(int(seq[0]), P2_TOTAL_CUPS, cup_cache)
        cup_cache[first_cup.value] = first_cup
        for c in seq[1:]:
            new_cup = Cup(int(c), P2_TOTAL_CUPS, cup_cache)
            cup_cache[new_cup.value] = new_cup
            new_cup.previous = cur_cup
            cur_cup.next = new_cup
            cur_cup = new_cup
        for i in range(10, P2_TOTAL_CUPS + 1):
            new_cup = Cup(i, P2_TOTAL_CUPS, cup_cache)
            cup_cache[new_cup.value] = new_cup
            new_cup.previous = cur_cup
            cur_cup.next = new_cup
            cur_cup = new_cup
        first_cup.previous = cur_cup
        cur_cup.next = first_cup
        return first_cup

    def yank_3(self) -> "Cup":
        held_cups = self.next
        last_cup = held_cups.next.next
        self.next = last_cup.next
        last_cup.next.previous = self
        held_cups.previous = None
        last_cup.next = None
        return held_cups

    def place_3(self, held_cups: "Cup"):
        last_cup = held_cups.next.next
        last_cup.next = self.next
        held_cups.previous = self
        self.next = held_cups
        last_cup.next.previous = last_cup

    def find_num(self, num: int) -> "Cup":
        if num < 1:
            num = self.max_val
        return self.cup_cache[num]

    def is_cup_in_next_3(self, cup: "Cup") -> bool:
        if cup is self:
            return True
        if cup is self.next:
            return True
        if cup is self.next.next:
            return True
        return False

    def run_round(self) -> "Cup":
        held_cups = self.yank_3()
        dest_cup = self.find_num(self.value - 1)
        while held_cups.is_cup_in_next_3(dest_cup):
            dest_cup = self.find_num(dest_cup.value - 1)
        dest_cup.place_3(held_cups)
        return self.next

    def state_to_str(self) -> str:
        one_cup = self.find_num(1)
        ret_str = ""
        next_cup = one_cup.next
        while next_cup is not one_cup:
            ret_str += str(next_cup.value)
            next_cup = next_cup.next
        return ret_str

    def get_p2_nums(self) -> Tuple[int, int]:
        one_cup = self.find_num(1)
        return one_cup.next.value, one_cup.next.next.value


def part_1(input_str: str):
    cur_cup = Cup.load_input(input_str)
    for _move in range(P1_RUNS):
        cur_cup = cur_cup.run_round()
    print(cur_cup.state_to_str())


def part_2(input_str: str):
    cur_cup = Cup.load_input_p2(input_str)
    for _move in range(P2_RUNS):
        cur_cup = cur_cup.run_round()
    n2, n3 = cur_cup.get_p2_nums()
    print(n2 * n3)


if __name__ == "__main__":
    part_1(DATA)
    part_2(DATA)
