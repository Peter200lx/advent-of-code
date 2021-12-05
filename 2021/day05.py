from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, NamedTuple

FILE_DIR = Path(__file__).parent


class Coord(NamedTuple):
    x: int
    y: int


def parse_input(lines: str) -> List[Tuple[Coord, Coord]]:
    dual_coords = [line.split(" -> ") for line in lines.split("\n")]
    return [
        (
            Coord(int(first.split(",")[0]), int(first.split(",")[1])),
            Coord(int(second.split(",")[0]), int(second.split(",")[1])),
        )
        for first, second in dual_coords
    ]


def solve(coord_pairs: List[Tuple[Coord, Coord]], part2: bool = False) -> int:
    seen_locs: Dict[Coord, int] = defaultdict(int)
    for first, second in coord_pairs:
        if first.x == second.x:
            points_on_line = (
                Coord(first.x, y)
                for y in range(min(first.y, second.y), max(first.y, second.y) + 1)
            )
            for point in points_on_line:
                seen_locs[point] += 1
        elif first.y == second.y:
            points_on_line = (
                Coord(x, first.y)
                for x in range(min(first.x, second.x), max(first.x, second.x) + 1)
            )
            for point in points_on_line:
                seen_locs[point] += 1
        elif part2:
            xdown = 1 if first.x < second.x else -1
            ydown = 1 if first.y < second.y else -1
            points_on_line = (
                Coord(x, y)
                for x, y in zip(
                    range(first.x, second.x + xdown, xdown),
                    range(first.y, second.y + ydown, ydown),
                )
            )
            for point in points_on_line:
                seen_locs[point] += 1
    return sum(v > 1 for v in seen_locs.values())


if __name__ == "__main__":
    DATA = (FILE_DIR / "day05.input").read_text().strip()

    VENT_LINES = parse_input(DATA)

    print(solve(VENT_LINES))
    print(solve(VENT_LINES, part2=True))
