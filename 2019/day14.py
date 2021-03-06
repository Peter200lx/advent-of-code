from math import ceil
from pathlib import Path
from typing import Dict, List

INPUT_FILE = Path(__file__).with_suffix(".input")


class Chemical:
    def __init__(self, my_name: str):
        self.name = my_name
        self.produced = None
        self.needs = None

    def set_reaction(self, inputs: Dict["Chemical", int], resulting_num: int):
        self.produced = resulting_num
        self.needs = inputs

    def find_required_base(
        self, required: int = 1, extras: Dict["Chemical", int] = None
    ) -> int:
        if self.needs is None:
            return required
        if extras is None:
            extras = {}
        if self in extras:
            extras[self] -= required
            if extras[self] >= 0:
                if extras[self] == 0:
                    del extras[self]
                return 0  # Didn't have to consume any base
            else:
                required = -extras[self]
                del extras[self]
        multiple = ceil(required / self.produced)
        extras[self] = (multiple * self.produced) - required
        used_base = 0
        for in_chem, needed in self.needs.items():
            used_base += in_chem.find_required_base(multiple * needed, extras)
        return used_base

    def __repr__(self) -> str:
        return (
            f"R({self.name}, {self.produced},"
            f" {[f'{k.name}-{v}' for k,v in self.needs.items()] if self.needs else 'none'})"
        )


def build_reactions(lines: List[str]) -> Dict[str, Chemical]:
    all_chem = {}
    for r_from, r_to in (line.split("=>") for line in lines):
        needs: Dict[Chemical, int] = {}
        for required, name in (p.split() for p in r_from.strip().split(",")):
            if name not in all_chem:
                all_chem[name] = Chemical(name)
            needs[all_chem[name]] = int(required)
        produced, name = r_to.strip().split()
        if name not in all_chem:
            all_chem[name] = Chemical(name)
        all_chem[name].set_reaction(needs, int(produced))
    return all_chem


def binary_search(fuel: Chemical, just_under_base: int) -> int:
    first = 0
    last = just_under_base
    while first != last:
        mid = (first + last) // 2
        used_base = fuel.find_required_base(mid)
        if used_base >= just_under_base:
            last = mid - 1
        else:
            first = mid + 1
    return first


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    reaction_list = DATA.split("\n")

    reactiondb = build_reactions(reaction_list)
    print(reactiondb["FUEL"].find_required_base())
    print(binary_search(reactiondb["FUEL"], 1_000_000_000_000))
