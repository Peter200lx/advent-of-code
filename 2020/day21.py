from collections import defaultdict
from functools import reduce
from pathlib import Path
from typing import List, NamedTuple


FILE_DIR = Path(__file__).parent


class Food(NamedTuple):
    ingredients: List[str]
    allergens: List[str]


def read_data(input_str: str) -> List[Food]:
    all_foods = []
    for line in input_str.split("\n"):
        unknown_str, allergen_str = line.split(" (contains ")
        unknown_words = unknown_str.split()
        allergens = allergen_str.rstrip(")").split(", ")
        all_foods.append(Food(unknown_words, allergens))
    return all_foods


def map_allergens(all_foods: List[Food]):
    allergen_possibles = {}
    for food in all_foods:
        for allergen in food.allergens:
            if allergen not in allergen_possibles:
                allergen_possibles[allergen] = set(food.ingredients)
            else:
                allergen_possibles[allergen] &= set(food.ingredients)

    can_be_allergens = reduce(set.union, allergen_possibles.values())
    are_not_allergens = {i for food in all_foods for i in food.ingredients} - can_be_allergens

    count = sum(ing in are_not_allergens for food in all_foods for ing in food.ingredients)
    print(count)

    inverted_possibilities = defaultdict(set)
    for allergen, ings in allergen_possibles.items():
        for ing in ings:
            inverted_possibilities[ing].add(allergen)

    locked_in = set()
    while any(len(v) > 1 for v in inverted_possibilities.values()):
        ing, possible = next((k, v) for k, v in inverted_possibilities.items() if len(v) == 1 and k not in locked_in)
        locked_in.add(ing)
        to_remove_i = next(iter(possible))
        for key in inverted_possibilities:
            if key == ing:
                continue
            inverted_possibilities[key].discard(to_remove_i)

    print(",".join((k for k, v in sorted(inverted_possibilities.items(), key=lambda x: next(iter(x[1]))))))


if __name__ == "__main__":
    DATA = (FILE_DIR / "day21.input").read_text().strip()
    FOODS = read_data(DATA)
    map_allergens(FOODS)
