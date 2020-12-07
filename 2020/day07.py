from pathlib import Path

FILE_DIR = Path(__file__).parent

SPECIAL_BAG = ("shiny", "gold")


class Bag:
    desc: str
    color: str

    def __init__(self, desc, color):
        self.desc = desc
        self.color = color
        self.parents = []
        self.children = []

    @property
    def id(self):
        return self.desc, self.color

    def __repr__(self):
        return f"Bag({self.desc}-{self.color}, p-{len(self.parents)}, c-{len(self.children)})"


def parse_lines(input_lines):
    all_bags = {}
    for line in input_lines.split("\n"):
        container, items = line.split(" contain ")
        c_desc, c_color, _bag = container.split()
        cont_bag = all_bags.setdefault((c_desc, c_color), Bag(c_desc, c_color))
        if "no other" in items:
            continue
        items = items.split(", ")
        for item in items:
            num, i_desc, i_color, _bag = item.split()
            i_bag = all_bags.setdefault((i_desc, i_color), Bag(i_desc, i_color))
            cont_bag.children.append((int(num), i_bag))
            i_bag.parents.append(cont_bag)
    return all_bags


def walk_tree(current_bag, visited_bags=None):
    if visited_bags is None:
        visited_bags = {current_bag.id}
    count = 0
    for parent in current_bag.parents:
        if parent.id not in visited_bags:
            visited_bags.add(parent.id)
            count += 1
            count += walk_tree(parent, visited_bags)
    return count


def part_two(current_bag):
    count = 1
    for num, child in current_bag.children:
        count += num * part_two(child)
    return count


if __name__ == "__main__":
    DATA = (FILE_DIR / "day07.input").read_text().strip()
    ALL_BAGS = parse_lines(DATA)
    print(walk_tree(ALL_BAGS[SPECIAL_BAG]))
    print(part_two(ALL_BAGS[SPECIAL_BAG]) - 1)  # -1 to not include starting bag
