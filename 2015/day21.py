import sys
from itertools import combinations
from typing import NamedTuple, Dict, List, Set, Tuple

DATA = """Hit Points: 109
Damage: 8
Armor: 2"""

ITEM_SHOP = """
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
"""


class Item(NamedTuple):
    type: str
    name: str
    cost: int
    damage: int
    armor: int


class Character:
    _starting_hp: int
    hp: int
    damage: int
    armor: int

    def __repr__(self):
        return f"{self.__class__.__name__}({self.hp}, {self.damage}, {self.armor})"

    def reset(self):
        self.hp = self._starting_hp

    def attack(self, other: "Character"):
        attack = self.damage - other.armor
        other.hp -= attack if attack > 0 else 1


class Player(Character):
    _starting_hp: int = 100
    items: Set[Item] = set()

    def reset(self):
        super().reset()
        self.items = set()
        self.damage = 0
        self.armor = 0

    def apply_item(self, item: Item):
        self.items.add(item)
        self.damage += item.damage
        self.armor += item.armor

    @property
    def cost(self) -> int:
        if not self.items:
            return 0
        return sum(i.cost for i in self.items)


class Boss(Character):
    def __init__(self, input_str):
        hp_str, dam_str, arm_str = input_str.split("\n")
        self._starting_hp = int(hp_str.split(": ")[1])
        self.damage = int(dam_str.split(": ")[1])
        self.armor = int(arm_str.split(": ")[1])
        self.reset()


def parse_item_shop(items_str) -> Dict[str, List[Item]]:
    items: Dict[str, List[Item]] = {}
    items_str = items_str.strip("\n")
    for item_type_str in items_str.split("\n\n"):
        title, *values = item_type_str.split("\n")
        item_type, *_ = title.split(":")
        items[item_type] = []
        cost_index = title.index("C")
        damage_index = title.index("D", cost_index)
        armor_index = title.index("A", damage_index)
        for item in values:
            items[item_type].append(
                Item(
                    item_type,
                    item[:cost_index].strip(),
                    int(item[cost_index:damage_index]),
                    int(item[damage_index:armor_index]),
                    int(item[armor_index:]),
                )
            )
    items["Armor"].append(Item("Armor", "Naked", 0, 0, 0))
    items["Rings"].extend([Item("Rings", "nada", 0, 0, 0)] * 2)
    return items


def play_war(player: Player, boss: Boss):
    while player.hp > 0 and boss.hp > 0:
        player.attack(boss)
        boss.attack(player)
    return player if boss.hp <= 0 else boss


def find_results(items: Dict[str, List[Item]], boss: Boss) -> Tuple[int, int]:
    player = Player()
    min_cost = sys.maxsize
    max_lost = 0
    for wep in items["Weapons"]:
        for arm in items["Armor"]:
            for ring_comb in combinations(items["Rings"], 2):
                player.reset()
                boss.reset()
                for item in (wep, arm, *ring_comb):
                    player.apply_item(item)
                if play_war(player, boss) is player:
                    min_cost = min(min_cost, player.cost)
                else:
                    max_lost = max(max_lost, player.cost)
    return min_cost, max_lost


if __name__ == "__main__":
    ITEMS = parse_item_shop(ITEM_SHOP)
    BOSS = Boss(DATA)
    part_1, part_2 = find_results(ITEMS, BOSS)
    print(part_1)
    print(part_2)
