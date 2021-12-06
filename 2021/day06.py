from pathlib import Path
from typing import List

FILE_DIR = Path(__file__).parent


def solve(fish_ages: List[int], days: int) -> int:
    count_of_fish_in_age = [fish_ages.count(i) for i in range(9)]
    # I really like the modulo approach from this ruby solution
    # https://www.reddit.com/r/adventofcode/comments/r9z49j/2021_day_6_solutions/hnfdhsi/
    for i in range(days):
        count_of_fish_in_age[(i + 7) % 9] += count_of_fish_in_age[i % 9]
    return sum(count_of_fish_in_age)


if __name__ == "__main__":
    DATA = (FILE_DIR / "day06.input").read_text().strip()
    AGES = [int(line) for line in DATA.split(",")]

    print(solve(AGES, 80))
    print(solve(AGES, 256))
