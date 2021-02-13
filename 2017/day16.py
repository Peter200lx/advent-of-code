from typing import List
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


def run_dance(list_inst: List[str], dance_order: List[str] = []) -> List[str]:
    if not dance_order:
        dance_order[:] = [chr(ord("a") + i) for i in range(16)]
    # print(dance_order)
    for inst in list_inst:
        if inst[0] == "s":
            num = int(inst[1:])
            # print(f"pre-swap {num:2}: {dance_order}")
            dance_order[:] = dance_order[-num:] + dance_order[:-num]
            # print(f"post-swap:   {dance_order}")
        elif inst[0] == "x":
            A, B = [int(x) for x in inst[1:].split("/")]
            # print(f"pre-exch {A:2}, {B:2}: {dance_order}")
            dance_order[A], dance_order[B] = dance_order[B], dance_order[A]
            # print(f"post-exch:       {dance_order}")
        elif inst[0] == "p":
            A, B = [dance_order.index(x) for x in inst[1:].split("/")]
            # print(f"pre-part {inst[1:]}: {dance_order}")
            dance_order[A], dance_order[B] = dance_order[B], dance_order[A]
            # print(f"post-part:    {dance_order}")
        else:
            raise Exception("Invalid instruction")
    return dance_order


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    INSTRUCTIONS = [s for s in DATA.split(",")]
    list_o_states = ["".join(run_dance(INSTRUCTIONS))]
    print(list_o_states[0])
    for _ in range(1000000000 - 1):
        result = "".join(run_dance(INSTRUCTIONS))
        if result == list_o_states[0]:
            break
        else:
            list_o_states.append(result)

    mod_val = len(list_o_states)
    print(mod_val)
    location = 1000000000 % mod_val

    print(list_o_states[(location - 1) % mod_val])
