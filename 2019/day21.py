from pathlib import Path
from typing import List

from processor import Processor


def run_bot(program: List[int], bot_instructions: List[str], debug: int = 0):
    running_bot = Processor(program).run_on_input_generator()
    output = next(running_bot)  # Move to first yield for .send(

    if debug:
        print("".join(chr(i) for i in output), end="")

    assert len(bot_instructions) <= 15
    input_str = "\n".join(bot_instructions) + "\n"

    if debug:
        print(input_str)
    try:
        i = 0
        output = []  # Stop Pycharm complaining about reference before assignment
        while i < len(input_str):
            output = running_bot.send(ord(input_str[i]))
            i += 1

        if debug:
            print("Done sending string")
            print("".join(chr(i) if i < 0x10FFFF else str(i) for i in output))
        return output[-1]

    except StopIteration:
        return NotImplementedError(f"Don't expect the bot to ever halt the program")


if __name__ == "__main__":
    DATA = Path("day21.input").read_text().strip()
    int_list = [int(i) for i in DATA.split(",")]

    p1 = [
        "NOT C T",
        "NOT B J",
        "OR T J",
        "NOT A T",
        "OR T J",  # _J == ~A | ~B | ~C
        "AND D J",  # J == ~(A & B & C) & D
        "WALK",
    ]
    print(run_bot(int_list, p1))
    p2 = [
        "NOT C T",
        "NOT B J",
        "OR T J",
        "NOT A T",
        "OR T J",
        "AND D J",  # J == ~(A & B & C) & D
        "NOT E T",
        "NOT T T",  # T == E
        "OR H T",  # _T == H | E
        "AND T J",  # J == ~(A & B & C) & D & (H | E)
        "RUN",
    ]
    print(run_bot(int_list, p2))
