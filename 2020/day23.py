from typing import Dict

DATA = """284573961"""
EXAMPLE_DATA = """389125467"""


class Cup:
    def __init__(self, value: int, cup_cache: Dict[int, "Cup"]):
        self.next: "Cup" = None
        self.previous: "Cup" = None
        self.value = value
        self.max_val = 9
        self.cup_cache = cup_cache

    @staticmethod
    def load_input(seq: str):
        cup_cache = {}
        cur_cup = first_cup = Cup(int(seq[0]), cup_cache)
        cup_cache[first_cup.value] = first_cup
        for c in seq[1:]:
            new_cup = Cup(int(c), cup_cache)
            cup_cache[new_cup.value] = new_cup
            new_cup.previous = cur_cup
            cur_cup.next = new_cup
            cur_cup = new_cup
        first_cup.previous = cur_cup
        cur_cup.next = first_cup
        return first_cup

    @staticmethod
    def load_input_p2(seq: str):
        cup_cache = {}
        cur_cup = first_cup = Cup(int(seq[0]), cup_cache)
        cup_cache[first_cup.value] = first_cup
        first_cup.max_val = 1_000_000
        for c in seq[1:]:
            new_cup = Cup(int(c), cup_cache)
            cup_cache[new_cup.value] = new_cup
            new_cup.max_val = 1_000_000
            new_cup.previous = cur_cup
            cur_cup.next = new_cup
            cur_cup = new_cup
        for i in range(10, 1_000_000 + 1):
            new_cup = Cup(i, cup_cache)
            cup_cache[new_cup.value] = new_cup
            new_cup.max_val = 1_000_000
            new_cup.previous = cur_cup
            cur_cup.next = new_cup
            cur_cup = new_cup
        first_cup.previous = cur_cup
        cur_cup.next = first_cup
        return first_cup

    def yank_3(self):
        held_cups = self.next
        last_cup = held_cups.next.next
        self.next = last_cup.next
        last_cup.next.previous = self
        held_cups.previous = None
        last_cup.next = None
        return held_cups

    def place_3(self, held_cups):
        last_cup = held_cups.next.next
        last_cup.next = self.next
        held_cups.previous = self
        self.next = held_cups
        last_cup.next.previous = last_cup

    def find_num(self, num: int):
        if num < 1:
            num = self.max_val
        return self.cup_cache[num]

    def is_cup_in_next_3(self, cup: "Cup"):
        if cup is self:
            return True
        if cup is self.next:
            return True
        if cup is self.next.next:
            return True
        return False

    def run_round(self):
        held_cups = self.yank_3()
        dest_cup = self.find_num(self.value - 1)
        while held_cups.is_cup_in_next_3(dest_cup):
            dest_cup = self.find_num(dest_cup.value - 1)
        dest_cup.place_3(held_cups)
        return self.next

    def print_state(self):
        one_cup = self.find_num(1)
        ret_str = ""
        next_cup = one_cup.next
        while next_cup != one_cup:
            ret_str += str(next_cup.value)
            next_cup = next_cup.next
        return ret_str

    def get_p2_nums(self):
        one_cup = self.find_num(1)
        return one_cup.next.value, one_cup.next.next.value


def part_1(input_str):
    cur_cup = Cup.load_input(input_str)
    for _move in range(100):
        cur_cup = cur_cup.run_round()
    print(cur_cup.print_state())


def part_2(input_str):
    cur_cup = Cup.load_input_p2(input_str)
    for _move in range(10_000_000):
        cur_cup = cur_cup.run_round()
    n2, n3 = cur_cup.get_p2_nums()
    print(n2 * n3)


if __name__ == "__main__":
    part_1(DATA)
    part_2(DATA)
