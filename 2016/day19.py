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


if __name__ == "__main__":
    ELF_RING = ElfNode.build_circle(int(DATA))
    WINNING_ELF = ELF_RING.run_game()
    print(WINNING_ELF.id)
    print(run_fixed_game(int(DATA)))
