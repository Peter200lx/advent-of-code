from pathlib import Path

from processor import Processor


def find_state(list_o_codes, desired_state):
    for noun in range(100):
        for verb in range(100):
            if (
                Processor(list_o_codes, ((1, noun), (2, verb))).run_no_io()
                == desired_state
            ):
                return noun, verb


if __name__ == "__main__":
    DATA = Path("day02.input").read_text().strip()
    int_list = [int(i) for i in DATA.split(",")]

    print(Processor(int_list, ((1, 12), (2, 2))).run_no_io())
    noun, verb = find_state(int_list, 19690720)
    print(f"{noun}{verb}")
