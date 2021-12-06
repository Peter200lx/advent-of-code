from pathlib import Path
from typing import List

FILE_DIR = Path(__file__).parent


def solve(fish_ages: List[int], days: int) -> int:
    count_of_fish_in_age = [fish_ages.count(i) for i in range(9)]
    for i in range(days):
        day_count = count_of_fish_in_age.pop(0)
        count_of_fish_in_age[6] += day_count
        count_of_fish_in_age.append(day_count)
    return sum(count_of_fish_in_age)


if __name__ == "__main__":
    DATA = (FILE_DIR / "day06.input").read_text().strip()
    AGES = [int(line) for line in DATA.split(",")]

    print(solve(AGES, 80))
    print(solve(AGES, 256))
