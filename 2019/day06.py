from pathlib import Path


class Planet:
    def __init__(self, value):
        self.value = value
        self.orbits = None
        self._depth = None

    @property
    def depth(self):
        if self._depth is not None:
            return self._depth
        if self.orbits is None:
            self._depth = 0
        else:
            self._depth = self.orbits.depth + 1
        return self._depth

    @property
    def orbits_set(self):
        ret_set = {self.value}
        if self.orbits:
            ret_set |= self.orbits.orbits_set
        return ret_set

    def find_shared_planet(self, other):
        if self.orbits is None:
            return None
        others_orbits_set = other.orbits_set
        next_orbit = self.orbits
        while next_orbit is not None:
            if next_orbit.value in others_orbits_set:
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


def part_1(all_planets):
    total_orbits = 0
    for planet in all_planets.values():
        total_orbits += planet.depth
    return total_orbits


def part_2(all_planets, first, second):
    p1 = all_planets[first].orbits
    p2 = all_planets[second].orbits
    connecting = p1.find_shared_planet(p2)
    return (p1.depth - connecting.depth) + (p2.depth - connecting.depth)


if __name__ == "__main__":
    DATA = Path("day06.input").read_text().strip()
    str_list = [line.split(")") for line in DATA.split("\n")]

    planets_dict = build_graph(str_list)
    print(part_1(planets_dict))
    print(part_2(planets_dict, "YOU", "SAN"))
