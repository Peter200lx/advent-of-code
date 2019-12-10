from itertools import permutations
from pathlib import Path

from processor import Processor


def test_day2():
    data = Path("day02.input").read_text().strip()
    int_list = [int(i) for i in data.split(",")]

    assert Processor(int_list, ((1, 12), (2, 2))).run_no_io() == 4023471

    def find_state(list_o_codes, desired_state):
        for noun in range(100):
            for verb in range(100):
                if (
                    Processor(list_o_codes, ((1, noun), (2, verb))).run_no_io()
                    == desired_state
                ):
                    return noun, verb

    assert find_state(int_list, 19690720) == (80, 51)


def test_day5():
    data = Path("day05.input").read_text().strip()
    int_list = [int(i) for i in data.split(",")]

    assert Processor(int_list).run([1])[-1] == 5182797
    assert Processor(int_list).run([5]) == [12077198]


def test_day7():
    data = Path("day07.input").read_text().strip()
    int_list = [int(i) for i in data.split(",")]

    def run_sequence(program, phase_nums):
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

    assert max(
        (run_sequence(int_list, p), p) for p in permutations((0, 1, 2, 3, 4))
    ) == (440880, (3, 2, 4, 0, 1))
    assert max(
        (run_sequence(int_list, p), p) for p in permutations((5, 6, 7, 8, 9))
    ) == (3745599, (5, 7, 9, 6, 8))


def test_day9():
    data = Path("day09.input").read_text().strip()
    int_list = [int(i) for i in data.split(",")]

    assert Processor(int_list).run([1]) == [3507134798]
    assert Processor(int_list).run([2]) == [84513]
