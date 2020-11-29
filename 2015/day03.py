from pathlib import Path
from typing import List, Tuple, Set

FILEDIR = Path(__file__).parent

DIRECTION_STRS = {"^": (-1, 0), "v": (1, 0), ">": (0, 1), "<": (0, -1)}
START = (0, 0)


def visited_locations(directions: List[str], already_visited: Set[Tuple[int]] = None) -> Set[Tuple[int]]:
    current_loc = START
    if already_visited is None:
        visited = {current_loc}
    else:
        visited = already_visited
    for direction in directions:
        current_loc = (current_loc[0] + DIRECTION_STRS[direction][0], current_loc[1] + DIRECTION_STRS[direction][1])
        visited.add(current_loc)
    return visited


if __name__ == "__main__":
    DATA = (FILEDIR / "day03.input").read_text().strip()
    print(len(visited_locations([x for x in DATA])))

    santa_dir = [x for i, x in enumerate(DATA) if i % 2]
    robo_dir = [x for i, x in enumerate(DATA) if not i % 2]
    combined_loc = visited_locations(santa_dir)
    combined_loc = visited_locations(robo_dir, combined_loc)
    print(len(combined_loc))
