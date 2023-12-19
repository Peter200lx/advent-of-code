from math import prod
from pathlib import Path
from typing import Dict, List, NamedTuple, Tuple, Optional

INPUT_FILE = Path(__file__).with_suffix(".input")

PART_VARS = {"a", "m", "x", "s"}


class Rule(NamedTuple):
    target: str
    var: Optional[str] = None
    op: Optional[str] = None
    val: Optional[int] = None


class Part:
    def __init__(self, in_str: str):
        self.vars = {s[0]: int(s[2:]) for s in in_str.strip("{}").split(",")}
        assert PART_VARS == self.vars.keys()


class PartRanges:
    def __init__(self, items: Dict[str, range]):
        assert PART_VARS == items.keys()
        self.vars = items

    def possible(self):
        return prod(len(v) for v in self.vars.values())

    def proc_ranges_lt(
        self, var: str, val: int
    ) -> Tuple[Optional["PartRanges"], Optional["PartRanges"]]:
        range_in_question = self.vars[var]
        if range_in_question.start < val and range_in_question.stop - 1 < val:
            return self, None
        if val in range_in_question:
            target = PartRanges(
                {
                    k: v if k != var else range(range_in_question.start, val)
                    for k, v in self.vars.items()
                }
            )
            self.vars[var] = range(val, range_in_question.stop)
            return target, self
        return None, self

    def proc_ranges_gt(
        self, var: str, val: int
    ) -> Tuple[Optional["PartRanges"], Optional["PartRanges"]]:
        range_in_question = self.vars[var]
        if range_in_question.start > val and range_in_question.stop - 1 > val:
            return self, None
        if val in range_in_question:
            target = PartRanges(
                {
                    k: v if k != var else range(val + 1, range_in_question.stop)
                    for k, v in self.vars.items()
                }
            )
            self.vars[var] = range(range_in_question.start, val + 1)
            return target, self
        return None, self

    def apply(self, rule: Rule) -> Tuple[Optional["PartRanges"], Optional["PartRanges"]]:
        if rule.op == "<":
            return self.proc_ranges_lt(rule.var, rule.val)
        return self.proc_ranges_gt(rule.var, rule.val)


def rule_apply_ranges(pr_list: List[PartRanges], rule: Rule) -> List[PartRanges]:
    assert rule.var is not None
    targ_list, keep_list = [], []
    for pr in pr_list:
        targ, keep = pr.apply(rule)
        if targ:
            targ_list.append(targ)
        if keep:
            keep_list.append(keep)
    pr_list[:] = keep_list
    return targ_list


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

    def find_target(self, part: Part):
        for rule in self.rules:
            if rule.var is None:
                return rule.target
            part_val = part.vars[rule.var]
            if rule.op == "<":
                if part_val < rule.val:
                    return rule.target
            elif rule.op == ">":
                if part_val > rule.val:
                    return rule.target

    def process_ranges(self, part_ranges: List[PartRanges]) -> Dict[str, List[PartRanges]]:
        destinations: Dict[str, List[PartRanges]] = {}
        for rule in self.rules:
            if rule.var is None:
                if rule.target == "R":
                    continue
            if rule.target == "R":
                dest = []
            else:
                if rule.target not in destinations:
                    destinations[rule.target] = []
                dest = destinations[rule.target]
            if rule.var is None:
                dest.extend(part_ranges)
                continue
            dest.extend(rule_apply_ranges(part_ranges, rule))
        return destinations


def part_one(workflows, parts):
    workflow_dict = {w.name: w for w in workflows}
    A = set()
    for part in parts:
        target = "in"
        while target not in {"A", "R"}:
            target = workflow_dict[target].find_target(part)
        if target == "A":
            A.add(part)
    return sum(sum(p.vars.values()) for p in A)


def part_two(workflows):
    workflow_dict = {w.name: w for w in workflows}
    A: List[PartRanges] = []
    to_proc: Dict[str, List[PartRanges]] = {
        "in": [PartRanges({l: range(1, 4001) for l in PART_VARS})]
    }
    while to_proc:
        name, list_of_ranges = to_proc.popitem()
        target_part_ranges = workflow_dict[name].process_ranges(list_of_ranges)
        if not target_part_ranges:  # Everything was rejected
            continue
        A.extend(target_part_ranges.pop("A", []))
        for target, list_of_ranges in target_part_ranges.items():
            if target in to_proc:
                to_proc[target].extend(list_of_ranges)
            else:
                to_proc[target] = list_of_ranges
    return sum(pr.possible() for pr in A)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    WORKFLOWSTR, PARTSTR = DATA.split("\n\n")

    WORKFLOWS = [Workflow(line) for line in WORKFLOWSTR.split("\n")]
    PARTS = [Part(line) for line in PARTSTR.split("\n")]

    print(part_one(WORKFLOWS, PARTS))
    print(part_two(WORKFLOWS))
