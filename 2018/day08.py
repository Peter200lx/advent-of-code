from pathlib import Path

FILE_DIR = Path(__file__).parent

EXAMPLE_DATA = """2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"""


class Node:
    def __init__(self, list_o_data, index=0):
        self.num_children = list_o_data[index]
        self.children = []
        self.num_meta = list_o_data[index + 1]
        index += 2
        for _ in range(self.num_children):
            child = Node(list_o_data, index)
            self.children.append(child)
            index = child.remaining_index
        self.meta = list_o_data[index : index + self.num_meta]
        self.remaining_index = index + self.num_meta

    def sum(self):
        ret_sum = 0
        for child in self.children:
            ret_sum += child.sum()
        ret_sum += sum(self.meta)
        return ret_sum

    def p2_sum(self):
        if not self.children:
            return sum(self.meta)
        ret_sum = 0
        for i in self.meta:
            if i > self.num_children or i <= 0:
                continue
            ret_sum += self.children[i - 1].p2_sum()
        return ret_sum


if __name__ == "__main__":
    DATA = (FILE_DIR / "day08.input").read_text().strip()

    int_input = [int(s) for s in DATA.split()]

    first_node = Node(int_input)
    print(first_node.sum())
    print(first_node.p2_sum())
