import re
from pathlib import Path
from typing import Dict, List, Tuple

FILE_DIR = Path(__file__).parent

REPLACEMENT_RULES = """8: 42 | 42 8
11: 42 31 | 42 11 31"""


def update_rule_dict(rule_dict: Dict[str, List[List[str]]], replacement_rules: str) -> Dict[str, List[List[str]]]:
    new_rules = rule_dict.copy()
    for line in replacement_rules.split("\n"):
        num, right = line.split(": ")
        new_rules[num] = [section.split() for section in right.split("|")]
    return new_rules


def read_input(lines: str) -> Tuple[Dict[str, List[List[str]]], List[str]]:
    rules_str, messages_str = lines.split("\n\n")
    rule_dict: Dict[str, List[List[str]]] = {}
    for line in rules_str.split("\n"):
        num, right = line.split(": ")
        rule_dict[num] = [section.split() for section in right.split("|")]
    messages = messages_str.split("\n")
    return rule_dict, messages


def build_rule(rules_dict: Dict[str, List[List[str]]], current_rule: str, depth: int = 0) -> str:
    rule = rules_dict[current_rule]
    sections = []
    for section in rule:
        section_regex = ""
        for label in section:
            if '"' in label:
                section_regex += label[1]
            else:
                if label == current_rule:
                    if depth < 5:
                        section_regex += build_rule(rules_dict, label, depth=depth + 1)
                else:
                    section_regex += build_rule(rules_dict, label, depth=depth)
        sections.append(section_regex)
    if len(sections) > 1:
        regex_str = f"{'|'.join(sections)}"
    else:
        regex_str = sections[0]
    return regex_str if len(regex_str) == 1 else f"({regex_str})"


def parse_messages(rules_dict: Dict[str, List[List[str]]], messages: List[str]) -> int:
    starting_rule = build_rule(rules_dict, "0")
    regex = re.compile(f"^{starting_rule}$")
    return sum(1 for m in messages if regex.match(m))


if __name__ == "__main__":
    DATA = (FILE_DIR / "day19.input").read_text().strip()
    RULES, MESSAGES = read_input(DATA)
    print(parse_messages(RULES, MESSAGES))
    UPDATED_RULES = update_rule_dict(RULES, REPLACEMENT_RULES)
    print(parse_messages(UPDATED_RULES, MESSAGES))
