from typing import Dict, Iterator
from pathlib import Path

import numpy as np

INPUT_FILE = Path(__file__).with_suffix(".input")

EXAMPLE_DATA = """../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#"""
START_PATTERN = """.#./..#/###"""


def pattern_to_array(pattern: str) -> np.ndarray:
    return np.array([[1 if c == "#" else 0 for c in line] for line in pattern.strip().split("/")])


def generate_possible_orientations(original_pattern: np.ndarray) -> Iterator[bytes]:
    yield original_pattern.tobytes()
    yield np.flipud(original_pattern).tobytes()
    yield np.fliplr(original_pattern).tobytes()
    local_pat = np.copy(original_pattern)
    for _ in range(3):
        local_pat = np.rot90(local_pat)
        yield local_pat.tobytes()
        yield np.flipud(local_pat).tobytes()
        yield np.fliplr(local_pat).tobytes()


def read_rules(full_data: str) -> Dict[bytes, np.ndarray]:
    result = {}
    for line in full_data.split("\n"):
        key, value = [pattern_to_array(str_arr) for str_arr in line.split(" => ")]
        for orientation in generate_possible_orientations(key):
            if orientation not in result:
                result[orientation] = value
    return result


def concat_arrays(old_arrray: np.ndarray, new_array: np.ndarray, axis: int) -> np.ndarray:
    if old_arrray is None:
        return new_array
    else:
        return np.concatenate((old_arrray, new_array), axis=axis)


def create_new_array_from_rules(combined_arr: np.ndarray, rule_dict: Dict[bytes, np.ndarray]) -> np.ndarray:
    if combined_arr.shape[0] % 2 == 0:
        chunk_size = 2
    elif combined_arr.shape[0] % 3 == 0:
        chunk_size = 3
    else:
        raise Exception(f"Unknown grid size {combined_arr.size}")
    chunks_per_row = combined_arr.shape[0] // chunk_size
    # Following logic from https://stackoverflow.com/a/16715845/1038644
    total_blocks = (
        combined_arr[j * chunk_size : (j + 1) * chunk_size, k * chunk_size : (k + 1) * chunk_size]
        for j, k in np.ndindex(chunks_per_row, chunks_per_row)
    )
    current_row = None
    new_array = None
    items_in_row = 0
    for section in total_blocks:
        # print(f"Old Section\n{section}")
        new_section = rule_dict[section.tobytes()]
        items_in_row += 1
        # print(f"New Section\n{new_section}")
        current_row = concat_arrays(current_row, new_section, axis=1)

        if items_in_row == chunks_per_row:
            items_in_row = 0
            new_array = concat_arrays(new_array, current_row, axis=0)
            current_row = None
    return new_array


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    start = pattern_to_array(START_PATTERN)
    # print(start)
    rules = read_rules(DATA)
    working_array = start
    for i in range(18):
        # print(working_array.shape)
        working_array = create_new_array_from_rules(working_array, rules)
        # print(f"Finished updating array {i + 1} times")
        # print(working_array)
        if i == 4:
            print(sum(sum(working_array)))
    print(sum(sum(working_array)))
