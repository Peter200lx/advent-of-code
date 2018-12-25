import re

DATA = """
Immune System:
2749 units each with 8712 hit points (immune to radiation, cold; weak to fire) with an attack that does 30 radiation damage at initiative 18
704 units each with 1890 hit points with an attack that does 26 fire damage at initiative 17
1466 units each with 7198 hit points (immune to bludgeoning; weak to slashing, cold) with an attack that does 44 bludgeoning damage at initiative 6
6779 units each with 11207 hit points with an attack that does 13 cold damage at initiative 4
1275 units each with 11747 hit points with an attack that does 66 cold damage at initiative 2
947 units each with 5442 hit points with an attack that does 49 radiation damage at initiative 3
4319 units each with 2144 hit points (weak to bludgeoning, fire) with an attack that does 4 fire damage at initiative 9
6315 units each with 5705 hit points with an attack that does 7 cold damage at initiative 16
8790 units each with 10312 hit points with an attack that does 10 fire damage at initiative 5
3242 units each with 4188 hit points (weak to cold; immune to radiation) with an attack that does 11 bludgeoning damage at initiative 14

Infection:
1230 units each with 11944 hit points (weak to cold) with an attack that does 17 bludgeoning damage at initiative 1
7588 units each with 53223 hit points (immune to bludgeoning) with an attack that does 13 cold damage at initiative 12
1887 units each with 40790 hit points (immune to radiation, slashing, cold) with an attack that does 43 fire damage at initiative 15
285 units each with 8703 hit points (immune to slashing) with an attack that does 60 slashing damage at initiative 7
1505 units each with 29297 hit points with an attack that does 38 fire damage at initiative 8
191 units each with 24260 hit points (immune to bludgeoning; weak to slashing) with an attack that does 173 cold damage at initiative 20
1854 units each with 12648 hit points (weak to fire, cold) with an attack that does 13 bludgeoning damage at initiative 13
1541 units each with 49751 hit points (weak to cold, bludgeoning) with an attack that does 62 slashing damage at initiative 19
3270 units each with 22736 hit points with an attack that does 13 slashing damage at initiative 10
1211 units each with 56258 hit points (immune to slashing, cold) with an attack that does 73 bludgeoning damage at initiative 11""".strip()

RE_NUMS = re.compile(r"-?\d+")

GOOD = "Good"
BAD = "Bad"


class FighterGroup:
    def __init__(self, team, num_units, unit_hp, immunities, weaknesses, attack_damage, attack_type, initiative):
        self.team = team
        self.num_units = num_units
        self.unit_hp = unit_hp
        self.immunities = immunities
        self.weaknesses = weaknesses
        self.attack_damage = attack_damage
        self.attack_type = attack_type
        self.initiative = initiative

    def copy(self, boostuple=None):
        boost = 0
        if boostuple:
            if self.team == boostuple[0]:
                boost = boostuple[1]
        return FighterGroup(
            self.team, self.num_units, self.unit_hp, self.immunities, self.weaknesses,
            self.attack_damage + boost, self.attack_type, self.initiative
        )

    @property
    def effective_power(self):
        return self.num_units * self.attack_damage

    @property
    def target_phase_attacker_sort(self):
        return self.effective_power, self.initiative

    def target_selection(self, all_groups):
        best_target = None
        for group in all_groups:
            if group.team == self.team:
                continue
            if self.attack_type in group.immunities:
                continue

            if best_target is None:
                best_target = group
                continue
            elif (self.attack_type in group.weaknesses
                  and self.attack_type not in best_target.weaknesses):
                best_target = group
                continue

            if group.effective_power > best_target.effective_power:
                best_target = group
            elif group.effective_power == best_target.effective_power:
                if group.initiative > best_target.initiative:
                    best_target = group
        return best_target

    def attacked_by(self, attacker):
        assert attacker.attack_type not in self.immunities
        multiplier = 2 if attacker.attack_type in self.weaknesses else 1
        attack_power = attacker.effective_power * multiplier
        units_killed = attack_power // self.unit_hp
        self.num_units -= units_killed
        return units_killed > 0

    def __repr__(self):
        return f"Group({self.team}, u{self.num_units}, hp{self.unit_hp}, i{self.immunities}," \
            f" w{self.weaknesses}, d{self.attack_damage}, {self.attack_type}, i{self.initiative})"


def parse_input(initial_state):
    armies = []
    army_team = GOOD
    for army in initial_state.split("\n\n"):
        for group in army.split("\n")[1:]:
            num_units, unit_hp, attack_damage, initiative = tuple(map(int, RE_NUMS.findall(group)))
            attack_type = group.split()[-5]
            weaknesses = []
            immunities = []
            try:
                attributes = group[group.index("(") + 1:group.index(")")]
                for att in (s.strip() for s in attributes.split(";")):
                    if att.startswith("weak"):
                        att = att.lstrip("weak to ")
                        att_list = weaknesses
                    elif att.startswith("immune"):
                        att = att.lstrip("immune to ")
                        att_list = immunities
                    else:
                        raise ValueError(f"Unknown attribute: {att}")
                    att_list.extend([s.strip() for s in att.split(",")])
            except ValueError:
                pass
            armies.append(FighterGroup(
                army_team, num_units, unit_hp, immunities, weaknesses, attack_damage, attack_type, initiative
            ))
        army_team = BAD
    return armies


def run_round(armies):
    armies.sort(key=lambda x: x.target_phase_attacker_sort, reverse=True)
    target_selection = {}
    targets = armies[:]
    for group in armies:
        target = group.target_selection(targets)
        if target:
            targets.remove(target)
            target_selection[group] = target

    attackers = sorted(armies, key=lambda x: x.initiative, reverse=True)
    any_killed = False
    for attacker in attackers:
        if attacker in armies and attacker in target_selection:
            target = target_selection[attacker]
            any_killed |= target.attacked_by(attacker)
            if target.num_units <= 0:
                armies.remove(target)

    if not any_killed:
        print("Stall Detected!")
        return False
    first_team = armies[0].team
    for group in armies:
        if group.team != first_team:
            return True
    return False


def part_1(armies):
    p1_army = [g.copy() for g in armies]
    while run_round(p1_army):
        # print(p1_army)
        pass
    # print(p1_army)
    return sum((a.num_units for a in p1_army))


def part_2(armies):
    boost = 1
    good_won = False
    test_armies = []
    while not good_won:
        # print(f"Starting a run with boost {boost}")
        test_armies = [g.copy((GOOD, boost)) for g in armies]

        while run_round(test_armies):
            # print(test_armies)
            pass
        boost += 1

        good_won = True
        for group in test_armies:
            if group.team == BAD:
                good_won = False
                break
    return sum((a.num_units for a in test_armies))


if __name__ == '__main__':
    deer_system = parse_input(DATA)
    print(part_1(deer_system))
    print(part_2(deer_system))
