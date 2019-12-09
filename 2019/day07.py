from itertools import permutations
from pathlib import Path
from typing import Sequence as Seq, List

from processor import Processor


def run_sequence(program: List[int], phase_nums: Seq[int]) -> int:
    assert len(phase_nums) == 5
    prog_out = 0
    processors = [
        Processor(program).run_on_output_generator(phase_nums[n]) for n in range(5)
    ]
    [next(proc) for proc in processors]  # Move to first yield to accept .send()
    while processors:
        prog_in = prog_out
        cur_proc = processors.pop(0)
        try:
            prog_out = cur_proc.send(prog_in)
            processors.append(cur_proc)
        except StopIteration:
            pass  # Don't put processor back in the loop after ProgramHalt

    return prog_out


if __name__ == "__main__":
    DATA = Path("day07.input").read_text().strip()
    int_list = [int(i) for i in DATA.split(",")]

    print(max((run_sequence(int_list, p), p) for p in permutations((0, 1, 2, 3, 4))))
    print(max((run_sequence(int_list, p), p) for p in permutations((5, 6, 7, 8, 9))))
