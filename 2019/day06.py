from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


class Planet:
    def __init__(self, value):
        self.value = value
        self.orbits = None

    @property
    def depth(self):
        return 0 if self.orbits is None else self.orbits.depth + 1

    @property
    def center_path(self):
        path = {self.value}
        return path if self.orbits is None else path | self.orbits.center_path

    def find_shared_planet(self, other):
        others_path = other.center_path
        next_orbit = self
        while next_orbit is not None:
            if next_orbit.value in others_path:
                return next_orbit
            next_orbit = next_orbit.orbits
        return None


def build_graph(orbits_list):
    parent_dict = {}
    for orbited, orbiting in orbits_list:
        if orbited not in parent_dict:
            parent_dict[orbited] = Planet(orbited)
        if orbiting not in parent_dict:
            parent_dict[orbiting] = Planet(orbiting)
        parent_dict[orbiting].orbits = parent_dict[orbited]
    return parent_dict


def part_2(all_planets, first, second):
    p1 = all_planets[first].orbits
    p2 = all_planets[second].orbits
    connecting = p1.find_shared_planet(p2)
    return (p1.depth - connecting.depth) + (p2.depth - connecting.depth)


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    str_list = [line.split(")") for line in DATA.split("\n")]

    planets_dict = build_graph(str_list)
    print(sum(p.depth for p in planets_dict.values()))
    print(part_2(planets_dict, "YOU", "SAN"))
