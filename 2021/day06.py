from pathlib import Path
from typing import List

FILE_DIR = Path(__file__).parent


def part1(fish_ages: List[int]) -> int:
    cur_list = fish_ages
    for day in range(80):
        new_list = [age - 1 for age in cur_list]
        new_fish = sum(age < 0 for age in new_list)
        new_list = [age if age >= 0 else 6 for age in new_list]
        cur_list = new_list + [8] * new_fish
    return len(cur_list)


def part2(fish_ages: List[int]) -> int:
    count_of_fish_in_age = [fish_ages.count(i) for i in range(9)]
    for i in range(256):
        day_count = count_of_fish_in_age.pop(0)
        count_of_fish_in_age[6] += day_count
        count_of_fish_in_age.append(day_count)
    return sum(count_of_fish_in_age)


if __name__ == "__main__":
    DATA = (FILE_DIR / "day06.input").read_text().strip()
    AGES = [int(line) for line in DATA.split(",")]

    print(part1(AGES))
    print(part2(AGES))
