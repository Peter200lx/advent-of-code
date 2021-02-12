import re
from collections import defaultdict, namedtuple
from typing import List, Set
from pathlib import Path

FILE_DIR = Path(__file__).parent

RE_NUMS = re.compile(r"-?\d+")

Coord = namedtuple("Coord", ["x", "y", "z", "t"])


def parse_input(instructions: str) -> List[Coord]:
    points = []
    for line in instructions.strip().split("\n"):
        points.append(Coord(*list(map(int, RE_NUMS.findall(line)))))
    return points


def calc_distance(loc1: Coord, loc2: Coord) -> int:
    return abs(loc1.x - loc2.x) + abs(loc1.y - loc2.y) + abs(loc1.z - loc2.z) + abs(loc1.t - loc2.t)


def part_1(list_o_stars: List[Coord]) -> List[Set[Coord]]:
    stars_within_range = defaultdict(set)
    for i, star1 in enumerate(list_o_stars):
        for star2 in list_o_stars[i + 1 :]:
            if calc_distance(star1, star2) <= 3:
                stars_within_range[star1].add(star2)

    constellations = []
    for star in list_o_stars:
        star_set = stars_within_range[star]
        star_set.add(star)

        found_constellations = []
        for i, const in enumerate(constellations):
            for neighbor_star in star_set:
                if neighbor_star in const:
                    found_constellations.append(i)
                    break
        if not found_constellations:
            found_const = set()
            constellations.append(found_const)
        else:
            first, *rest = found_constellations
            rest.sort(reverse=True)
            found_const = constellations[first]
            for i in rest:
                found_const |= constellations[i]
                del constellations[i]
        found_const |= star_set

    return constellations


if __name__ == "__main__":
    DATA = (FILE_DIR / "day25.input").read_text().strip()
    print(len(part_1(parse_input(DATA))))
