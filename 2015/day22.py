import sys
from typing import NamedTuple, Dict

DATA = """Hit Points: 55
Damage: 8"""
PLAYER_HP = 50
PLAYER_MANA = 500


class Spell(NamedTuple):
    name: str
    cost: int
    damage: int = 0
    heal: int = 0
    length: int = 0
    armor: int = 0
    mana_gain: int = 0


SPELLS = [
    Spell("Magic Missile", 53, damage=4),
    Spell("Drain", 73, damage=2, heal=2),
    Spell("Shield", 113, length=6, armor=7),
    Spell("Poison", 173, length=6, damage=3),
    Spell("Recharge", 229, length=5, mana_gain=101),
]


def run_turn(
    b_hp: int,
    b_d: int,
    p_hp: int = PLAYER_HP,
    p_m: int = PLAYER_MANA,
    effects: Dict[Spell, int] = None,
    player_turn: bool = True,
    depth: int = 20,
    hard_mode: bool = False,
):
    if depth < 0:
        return sys.maxsize
    depth -= 1
    player_armor = 0
    if effects:
        new_effects = effects.copy()
        for spell, count in effects.items():
            if count == 1:
                del new_effects[spell]
            else:
                new_effects[spell] -= 1
            b_hp -= spell.damage
            p_m += spell.mana_gain
            player_armor += spell.armor
    else:
        new_effects = {}

    if b_hp <= 0:
        return 0

    if player_turn:
        if hard_mode:
            p_hp -= 1
        mana_cost = sys.maxsize
        for spell in SPELLS:
            if spell.cost > p_m or spell in new_effects:
                continue
            try_effects = {**new_effects, spell: spell.length} if spell.length else new_effects
            try_b_hp = b_hp - (0 if spell.length else spell.damage)
            mana_cost = min(
                mana_cost,
                spell.cost
                + run_turn(try_b_hp, b_d, p_hp + spell.heal, p_m - spell.cost, try_effects, False, depth, hard_mode),
            )
        return mana_cost
    else:  # boss turn
        damage = b_d - player_armor
        if damage <= 0:
            damage = 1
        p_hp -= damage
        if p_hp <= 0:
            return sys.maxsize
        return run_turn(b_hp, b_d, p_hp, p_m, new_effects, True, depth, hard_mode)


if __name__ == "__main__":
    BOSS_HP, BOSS_DAMAGE = [int(line.split(":")[1]) for line in DATA.split("\n")]
    print(run_turn(BOSS_HP, BOSS_DAMAGE))
    print(run_turn(BOSS_HP, BOSS_DAMAGE, hard_mode=True))
