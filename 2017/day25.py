from collections import defaultdict
from typing import Tuple, Dict, NamedTuple, List
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

EXAMPLE_DATA = """Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A."""


class StateLogic(NamedTuple):
    write: int
    move: int
    next_state: str


def parse_input(raw_str: str) -> Tuple[int, str, Dict[str, List[StateLogic]]]:
    control_dict = {}
    instructions = raw_str.split("\n")
    start_state = instructions[0].split()[-1].rstrip(".")
    num_steps = int(instructions[1].split()[-2])
    cur_line = 2
    while cur_line < len(instructions):
        if instructions[cur_line].startswith("In state"):
            cur_state = instructions[cur_line].split()[-1].rstrip(":")
            state_instructions = []
            for j in range(2):
                value = int(instructions[cur_line + 4 * j + 2].split()[-1].rstrip("."))
                move = -1 if instructions[cur_line + 4 * j + 3].split()[-1] == "left." else 1
                next_state = instructions[cur_line + 4 * j + 4].split()[-1].rstrip(".")
                state_instructions.append(StateLogic(value, move, next_state))
            assert cur_state not in control_dict
            control_dict[cur_state] = state_instructions
            cur_line += 8
        cur_line += 1
    return num_steps, start_state, control_dict


def step_machine(
    control_dict: Dict[str, List[StateLogic]], tape: Dict[int, int], cur_state: str, cur_loc: int
) -> Tuple[int, str]:
    current_value = tape[cur_loc]
    inst = control_dict[cur_state][current_value]
    tape[cur_loc] = inst.write
    return cur_loc + inst.move, inst.next_state


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    run_time, state, cont_dict = parse_input(DATA)
    tape_dict = defaultdict(int)
    location = 0
    print(run_time, state, location, cont_dict)
    for i in range(run_time):
        location, state = step_machine(cont_dict, tape_dict, state, location)
        if i % 1000000 == 0:
            print(location, state)
    print(sum(tape_dict.values()))
