from itertools import permutations
from pathlib import Path
from typing import Sequence as Seq, Tuple, Generator

from day02 import ProgramHalt
from day05 import D5Processor


class D7Processor(D5Processor):
    def run_on_output_generator(self, phase: int) -> Generator[int, int, None]:
        ip = 0
        self.input.append(phase)
        first_input = yield
        self.input.append(first_input)
        try:
            while True:
                ip = self.func_by_instruction_pointer(ip)
                if self.output:
                    new_input = yield self.output.pop(0)
                    self.input.append(new_input)
        except ProgramHalt:
            return None


def run_sequence(program: Seq[int], phase_nums: Seq[int]) -> int:
    assert len(phase_nums) == 5
    prog_out = 0
    processors = [
        D7Processor(program).run_on_output_generator(phase_nums[n]) for n in range(5)
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


def test_all_seq(program: Seq[int], part2: bool = False) -> Tuple[int, Seq[int]]:
    maximum = 0
    best = None
    base_list = (0, 1, 2, 3, 4) if not part2 else (5, 6, 7, 8, 9)
    for phase_seq in permutations(base_list, 5):
        result = run_sequence(program, phase_seq)
        if result > maximum:
            # print(f"old_max {maximum}, new_max {result} for {phase_seq}")
            maximum = result
            best = phase_seq
    return maximum, best


if __name__ == "__main__":
    DATA = Path("day07.input").read_text().strip()
    int_list = [int(i) for i in DATA.split(",")]

    print(test_all_seq(int_list))
    print(test_all_seq(int_list, part2=True))
