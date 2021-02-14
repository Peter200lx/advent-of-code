from itertools import combinations
from pathlib import Path
from typing import List

from processor import Processor

INPUT_FILE = Path(__file__).with_suffix(".input")


def run_sequence(running_bot, input_cmds, debug):
    if debug:
        print(input_cmds)
    for c in input_cmds:
        output = running_bot.send(ord(c))
        if output:
            out_str = "".join(chr(i) for i in output)
            if debug:
                print(out_str)


def try_items(running_bot, items, debug):
    input_cmds = "\n".join(f"drop {item}" for item in items) + "\n"
    run_sequence(running_bot, input_cmds, debug)
    out_str = ""
    for i in range(len(items), 0, -1):
        for item_comb in combinations(items, i):
            input_cmds = "\n".join(f"take {item}" for item in item_comb) + "\n"
            run_sequence(running_bot, input_cmds, debug)
            for c in "west\n":
                output = running_bot.send(ord(c))
                if output:
                    out_str = "".join(chr(i) for i in output)
                    if debug:
                        print(out_str)
            if "Alert!" in out_str:
                input_cmds = "\n".join(f"drop {item}" for item in item_comb) + "\n"
                run_sequence(running_bot, input_cmds, debug)
            else:
                return input_cmds + out_str
    raise NotImplementedError("Didn't find a valid combination")


def run_bot(program: List[int], debug: int = 0):
    running_bot = Processor(program).run_on_input_generator()
    output = next(running_bot)  # Move to first yield for .send(

    print("".join(chr(i) for i in output))

    starting_sequence = [
        "west",
        "take whirled peas",
        "east",
        "south",
        "west",
        "take bowl of rice",
        "east",
        "east",
        "take mutex",
        "east",
        "take astronaut ice cream",
        "east",
        "take ornament",
        "west",
        "south",
        "take tambourine",
        "north",
        "west",
        "south",
        "east",
        "take mug",
        "west",
        "south",
        "west",
        "south",
        "take easter egg",
        "west",
    ]
    items = [
        "bowl of rice",
        "easter egg",
        "tambourine",
        "astronaut ice cream",
        "mug",
        "mutex",
        "whirled peas",
        "ornament",
    ]
    i = 0
    all_input = []
    input_str = ""
    try:
        output = []  # Stop Pycharm complaining about reference before assignment
        while True:
            if len(output) != 0:
                print("".join(chr(i) for i in output), end="")
            if i >= len(input_str):
                i = 0
                input_str = input("")
                if "dump run" in input_str:
                    print(all_input)
                    return
                elif "auto run start" in input_str:
                    input_str = "\n".join(starting_sequence)
                elif "auto run door" in input_str:
                    return try_items(running_bot, items, debug)
                else:
                    all_input.append(input_str)
                if not input_str.endswith("\n"):
                    input_str += "\n"
            output = running_bot.send(ord(input_str[i]))
            i += 1

    except StopIteration:
        return NotImplementedError(f"Don't expect the bot to ever halt the program")


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    int_list = [int(i) for i in DATA.split(",")]

    print(run_bot(int_list))
