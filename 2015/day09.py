from typing import Dict, Set, Optional

DATA = """Faerun to Norrath = 129
Faerun to Tristram = 58
Faerun to AlphaCentauri = 13
Faerun to Arbre = 24
Faerun to Snowdin = 60
Faerun to Tambi = 71
Faerun to Straylight = 67
Norrath to Tristram = 142
Norrath to AlphaCentauri = 15
Norrath to Arbre = 135
Norrath to Snowdin = 75
Norrath to Tambi = 82
Norrath to Straylight = 54
Tristram to AlphaCentauri = 118
Tristram to Arbre = 122
Tristram to Snowdin = 103
Tristram to Tambi = 49
Tristram to Straylight = 97
AlphaCentauri to Arbre = 116
AlphaCentauri to Snowdin = 12
AlphaCentauri to Tambi = 18
AlphaCentauri to Straylight = 91
Arbre to Snowdin = 129
Arbre to Tambi = 53
Arbre to Straylight = 40
Snowdin to Tambi = 15
Snowdin to Straylight = 99
Tambi to Straylight = 70"""


class City:
    def __init__(self, my_id: str):
        self.id = my_id
        self.neighbors: Dict["City", int] = {}

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"City({self.id})"

    def shortest(self, visited: Optional[Set["City"]] = None) -> int:
        if visited is None:
            visited = {self}
        if len(visited) == len(self.neighbors) + 1:
            return 0
        return min(
            dist + city.shortest(visited | {city}) for city, dist in self.neighbors.items() if city not in visited
        )

    def longest(self, visited: Optional[Set["City"]] = None) -> int:
        if visited is None:
            visited = {self}
        if len(visited) == len(self.neighbors) + 1:
            return 0
        return max(
            dist + city.longest(visited | {city}) for city, dist in self.neighbors.items() if city not in visited
        )


def load_input(input_str: str):
    all_cities: Dict[str, City] = {}
    for line in input_str.split("\n"):
        locs, dist = line.split(" = ")
        a, b = locs.split(" to ")
        city_a = all_cities.setdefault(a, City(a))
        city_b = all_cities.setdefault(b, City(b))
        city_a.neighbors[city_b] = int(dist)
        city_b.neighbors[city_a] = int(dist)
    return all_cities


if __name__ == "__main__":
    CITIES = load_input(DATA)
    print(min(c.shortest() for c in CITIES.values()))
    print(max(c.longest() for c in CITIES.values()))
