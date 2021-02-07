DATA = """3017957"""


class ElfNode:
    def __init__(self, elf_num: int):
        self.id = elf_num
        self.next = self

    @staticmethod
    def build_circle(total_elves: int) -> "ElfNode":
        starting_elf = current_elf = ElfNode(1)
        for i in range(2, total_elves + 1):
            current_elf.next = ElfNode(i)
            current_elf = current_elf.next
        current_elf.next = starting_elf
        return starting_elf

    def run_game(self) -> "ElfNode":
        current_elf = self
        while current_elf.next != current_elf:
            stolen_elf = current_elf.next
            current_elf.next = stolen_elf.next
            current_elf = current_elf.next
        return current_elf


def run_fixed_game(num_elves: int):
    all_elves = list(range(1, num_elves + 1))
    current_index = 0
    while len(all_elves) > 1:
        steal_index = current_index + len(all_elves) // 2
        steal_index %= len(all_elves)
        assert steal_index != current_index
        del all_elves[steal_index]
        if steal_index > current_index:
            current_index += 1
        current_index %= len(all_elves)
    return all_elves[0]


def find_largest_power(n: int, base: int) -> int:
    for i in range(99999):
        if base ** i > n:
            return base ** (i - 1)


def guess_number(n: int) -> int:
    largest_power = find_largest_power(n, 3)
    guess = n - largest_power
    if guess == 0:
        return n
    elif guess > largest_power:
        return largest_power + (guess - largest_power) * 2
    return guess


def find_pattern(size: int = 300):
    for i in range(1, size):
        ans = run_fixed_game(i)
        guess = guess_number(i)
        print(f"{i:3} == {ans:3} guess {guess:3}")


if __name__ == "__main__":
    NUMBER_OF_ELVES = int(DATA)
    ELF_RING = ElfNode.build_circle(NUMBER_OF_ELVES)
    WINNING_ELF = ELF_RING.run_game()
    print(WINNING_ELF.id)
    # print(run_fixed_game(NUMBER_OF_ELVES))
    print(guess_number(NUMBER_OF_ELVES))
    # find_pattern()
