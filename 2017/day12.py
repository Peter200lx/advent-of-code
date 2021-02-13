import re
from typing import List, Set
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

PIPE_REGEX = re.compile(r"(\d*) <-> ([0-9, ]*)")

EXAMPLE_DATA = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""


def build_pipe_set_list(data: str) -> List[Set[int]]:
    pipe_set_list = []
    for line in data.split("\n"):
        current, targets = PIPE_REGEX.findall(line)[0]
        pipes = {int(s.strip()) for s in targets.split(",")}
        # print(f"pipe {current} should connect to {pipes}")
        pipes.add(int(current))
        found = None
        for pipe_set in pipe_set_list:
            if any(x in pipe_set for x in pipes):
                if found is None:
                    pipe_set.update(pipes)
                    found = pipe_set
                else:
                    found.update(pipe_set)
                    pipe_set_list.remove(pipe_set)

        if found is None:
            pipe_set_list.append(pipes)

    return pipe_set_list


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    PIPE_SET_LIST = build_pipe_set_list(DATA)
    SET_WITH_0 = next(pset for pset in PIPE_SET_LIST if 0 in pset)
    print(f"Number of programs in set with p0: {len(SET_WITH_0)}")
    print(f"Total number of groups: {len(PIPE_SET_LIST)}")
