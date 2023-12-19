from math import prod
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Tuple

INPUT_FILE = Path(__file__).with_suffix(".input")

PART_VARS = {"a", "m", "x", "s"}


class Rule(NamedTuple):
    target: str
    var: Optional[str] = None
    op: Optional[str] = None
    val: Optional[int] = None


class PartR:
    def __init__(self, items: Dict[str, range]):
        assert PART_VARS == items.keys()
        self._vars = items

    def possible(self):
        return prod(len(v) for v in self._vars.values())

    def proc_ranges_lt(self, var: str, val: int) -> Tuple[Optional["PartR"], Optional["PartR"]]:
        range_in_question = self._vars[var]
        if range_in_question.start < val and range_in_question.stop - 1 < val:
            return self, None
        if val in range_in_question:
            target = PartR(
                {
                    k: v if k != var else range(range_in_question.start, val)
                    for k, v in self._vars.items()
                }
            )
            self._vars[var] = range(val, range_in_question.stop)
            return target, self
        return None, self

    def proc_ranges_gt(self, var: str, val: int) -> Tuple[Optional["PartR"], Optional["PartR"]]:
        range_in_question = self._vars[var]
        if range_in_question.start > val and range_in_question.stop - 1 > val:
            return self, None
        if val in range_in_question:
            target = PartR(
                {
                    k: v if k != var else range(val + 1, range_in_question.stop)
                    for k, v in self._vars.items()
                }
            )
            self._vars[var] = range(range_in_question.start, val + 1)
            return target, self
        return None, self

    def apply(self, rule: Rule) -> Tuple[Optional["PartR"], Optional["PartR"]]:
        if rule.op == "<":
            return self.proc_ranges_lt(rule.var, rule.val)
        return self.proc_ranges_gt(rule.var, rule.val)


class Workflow:
    def __init__(self, in_str: str):
        self.name, rest = in_str.strip("}").split("{")
        rule_strs = rest.split(",")
        self.rules = []
        for rulestr in rule_strs:
            if ":" not in rulestr:
                self.rules.append(Rule(rulestr))
                continue
            cond, target = rulestr.split(":")
            self.rules.append(Rule(target, cond[0], cond[1], int(cond[2:])))

    def find_target(self, part: Dict[str, int]):
        for rule in self.rules:
            if rule.var is None:
                return rule.target
            part_val = part[rule.var]
            if rule.op == "<":
                if part_val < rule.val:
                    return rule.target
            elif rule.op == ">":
                if part_val > rule.val:
                    return rule.target

    def process_ranges(self, part_ranges: List[PartR]) -> Dict[str, List[PartR]]:
        destinations: Dict[str, List[PartR]] = {}
        for rule in self.rules:
            dest = [] if rule.target == "R" else destinations.setdefault(rule.target, [])
            if rule.var is None:
                dest.extend(part_ranges)
                continue
            keep_list = []
            for pr in part_ranges:
                targ, keep = pr.apply(rule)
                if targ:
                    dest.append(targ)
                if keep:
                    keep_list.append(keep)
            part_ranges = keep_list
        return destinations


def part_one(workflows: List[Workflow], parts: List[Dict[str, int]]) -> int:
    workflow_dict = {w.name: w for w in workflows}
    accepted = []
    for part in parts:
        target = "in"
        while target not in {"A", "R"}:
            target = workflow_dict[target].find_target(part)
        if target == "A":
            accepted.append(part)
    return sum(sum(p.values()) for p in accepted)


def part_two(workflows: List[Workflow]) -> int:
    workflow_dict = {w.name: w for w in workflows}
    accepted: List[PartR] = []
    to_proc: Dict[str, List[PartR]] = {"in": [PartR({l: range(1, 4001) for l in PART_VARS})]}
    while to_proc:
        name, list_of_ranges = to_proc.popitem()
        target_part_ranges = workflow_dict[name].process_ranges(list_of_ranges)
        accepted.extend(target_part_ranges.pop("A", []))
        for target, list_of_ranges in target_part_ranges.items():
            if target in to_proc:
                to_proc[target].extend(list_of_ranges)
            else:
                to_proc[target] = list_of_ranges
    return sum(pr.possible() for pr in accepted)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    WORKFLOWSTR, PARTSTR = DATA.split("\n\n")

    WORKFLOWS = [Workflow(line) for line in WORKFLOWSTR.split("\n")]
    PARTS = [
        {s[0]: int(s[2:]) for s in line.strip("{}").split(",")} for line in PARTSTR.split("\n")
    ]

    print(part_one(WORKFLOWS, PARTS))
    print(part_two(WORKFLOWS))
