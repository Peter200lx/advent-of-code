from pathlib import Path
from typing import Tuple, List, Dict, Optional, Set

FILE_DIR = Path(__file__).parent

SPECIAL_BAG = ("shiny", "gold")


class Bag:
    def __init__(self, desc: str, color: str):
        self.desc = desc
        self.color = color
        self.parents: List["Bag"] = []
        self.children: List[Tuple[int, "Bag"]] = []

    @property
    def id(self) -> Tuple[str, str]:
        return self.desc, self.color

    def __repr__(self) -> str:
        return f"Bag({self.desc}-{self.color}, p-{len(self.parents)}, c-{len(self.children)})"


def parse_lines(input_lines: str) -> Dict[Tuple[str, str], Bag]:
    all_bags: Dict[Tuple[str, str], Bag] = {}
    for line in input_lines.split("\n"):
        container, items = line.split(" contain ")
        if "no other" in items:
            continue
        c_desc, c_color, _bag = container.split()
        cont_bag = Bag(c_desc, c_color)
        cont_bag = all_bags.setdefault(cont_bag.id, cont_bag)
        for item in items.split(", "):
            num, i_desc, i_color, _bag = item.split()
            i_bag = Bag(i_desc, i_color)
            i_bag = all_bags.setdefault(i_bag.id, i_bag)
            cont_bag.children.append((int(num), i_bag))
            i_bag.parents.append(cont_bag)
    return all_bags


def uniq_parents(current_bag: Bag, visited_bags: Optional[Set[Tuple[str, str]]] = None) -> int:
    if visited_bags is None:
        visited_bags = {current_bag.id}
    count = 0
    for parent in current_bag.parents:
        if parent.id not in visited_bags:
            visited_bags.add(parent.id)
            count += 1
            count += uniq_parents(parent, visited_bags)
    return count


def count_children(current_bag: Bag) -> int:
    count = 0
    for num, child in current_bag.children:
        count += num * (1 + count_children(child))
    return count


if __name__ == "__main__":
    DATA = (FILE_DIR / "day07.input").read_text().strip()
    ALL_BAGS = parse_lines(DATA)
    starting_bag = ALL_BAGS[SPECIAL_BAG]
    print(uniq_parents(starting_bag))
    print(count_children(starting_bag))
