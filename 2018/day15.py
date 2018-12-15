from collections import namedtuple
from copy import copy

import numpy as np

DATA = """
################################
################.#.#..##########
################.#...G##########
################...#############
######..##########.#..##########
####.G...#########.G...#########
###.........######....##########
##..#.##.....#....#....#########
#G.#GG..................##.#####
##.##..##..G........G.........##
#######......G.G...............#
#######........................#
########.G....#####..E#...E.G..#
#########G...#######...........#
#########...#########.........##
#####.......#########....G...###
###.........#########.....E..###
#...........#########.........##
#..#....G..G#########........###
#..#.........#######.........###
#G.##G......E.#####...E..E..####
##......E...............########
#.....#G.G..............E..#####
#....#####....E........###.#####
#...#########.........####.#####
#.###########......#.#####.#####
#....##########.##...###########
#....#############....##########
##.##############E....##########
##.##############..#############
##....##########################
################################""".lstrip().split("\n")

EXAMPLE_DATA = """
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######""".lstrip().split("\n")

EXAMPLE_DATA2 = """
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######""".lstrip().split("\n")

EXAMPLE_DATA3 = """
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######""".lstrip().split("\n")

EXAMPLE_DATA4 = """
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######""".lstrip().split("\n")

EXAMPLE_DATA5 = """
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######""".lstrip().split("\n")

EXAMPLE_DATA6 = """
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########""".lstrip().split("\n")

np.set_printoptions(linewidth=300, threshold=np.nan, formatter={'int': lambda x: f"{x:2}" if x >= -1 else "██"})
Coord = namedtuple("Coord", ["y", "x"])


class P2Exception(Exception):
    pass


class Creature:
    def __init__(self, species, location, creature_dict, attack=3, hp=200):
        self.species = species
        self.loc = location
        self.attack = attack
        self.hp = hp

        self.all_creatures = creature_dict

        self.part_2 = False

    def __repr__(self):
        return f"{self.species}({self.loc} {self.hp})"

    @property
    def friends(self):
        return {l: c for l, c in self.all_creatures.items() if c.species == self.species}

    def friendly_hp(self):
        return sum(c.hp for c in self.friends.values())

    @property
    def foes(self):
        return {l: c for l, c in self.all_creatures.items() if c.species != self.species}

    def adjacent_foe(self, board):
        foe_locs = [(self.foes[l].hp, l) for l in adjacent_locs(board, self.loc) if l in self.foes]
        if foe_locs:
            foe_locs.sort()
            return self.foes[foe_locs[0][1]]
        return False

    def paths_to(self, board, loc):
        loc_board = board.copy()
        loc_board[loc_board == 0] = -1
        for c_loc in self.all_creatures:
            if c_loc != self.loc:
                loc_board[c_loc.y, c_loc.x] = -2
        simulate_water(loc_board, {loc}, 0)
        return loc_board

    def select_destination(self, board):
        possible_locs = []
        my_paths = self.paths_to(board, self.loc)
        for foe_loc in self.foes:
            foe_adjacent = adjacent_locs(board, foe_loc)
            for loc in foe_adjacent:
                if loc not in self.all_creatures:
                    weight = my_paths[loc.y, loc.x]
                    if weight >= 0:
                        possible_locs.append((weight, loc))

        if not possible_locs:
            return False

        possible_locs.sort()
        return possible_locs[0][1]

    def move_towards(self, board, destination):
        possible_moves = adjacent_locs(board, self.loc)
        dest_path = self.paths_to(board, destination)
        # print(dest_path)
        weighted_moves = [(dest_path[l.y, l.x], l) for l in possible_moves if l not in self.all_creatures]
        if not weighted_moves:
            # print_board(self.board, self.all_creatures)
            return
        weight, new_loc = sorted([t for t in weighted_moves if t[0] >= 0])[0]
        del self.all_creatures[self.loc]
        self.all_creatures[new_loc] = self
        self.loc = new_loc

    def take_turn(self, board):
        if not self.foes:
            return False
        if not self.adjacent_foe(board):
            destination = self.select_destination(board)
            if destination:
                self.move_towards(board, destination)
        adjacent_foe = self.adjacent_foe(board)
        if adjacent_foe:
            adjacent_foe.attacked(board, self.attack)
        return True

    def attacked(self, board, damage):
        self.hp -= damage
        if self.hp < 0:
            if self.part_2 and self.species == "E":
                raise P2Exception(f"{self} just died, reset and up the power!")
            # print(self)
            # print_board(board, self.all_creatures)
            del self.all_creatures[self.loc]


def adjacent_locs(base_board, loc):
    locs = [Coord(loc.y, x) for x in range(loc.x - 1, loc.x + 2, 2) if base_board[loc.y, x] >= -1]
    locs.extend([Coord(y, loc.x) for y in range(loc.y - 1, loc.y + 2, 2) if base_board[y, loc.x] >= -1])
    return locs


def simulate_water(board, check_locs, cost):
    # print(f"{cost}-> {check_locs}")
    next_locs = set()
    for loc in check_locs:
        if board[loc.y, loc.x] >= 0:
            continue
        board[loc.y, loc.x] = cost
        next_locs |= set(adjacent_locs(board, loc))
    next_locs = {l for l in next_locs if l not in check_locs}
    # print(f"next_locs: {next_locs}")
    if next_locs:
        simulate_water(board, next_locs, cost + 1)



# def build_paths(base_board, paths):
#     for y, x in np.argwhere(base_board == 0):
#         loc = Coord(y, x)
#         loc_board = base_board.copy()
#         loc_board[loc_board == 0] = -1
#         simulate_water(loc_board, {loc}, 0)
#         paths[loc] = loc_board


def parse_board(board_str_list):
    npcs = {}
    for y, line in enumerate(board_str_list):
        for x, c in enumerate(line):
            if c in ("E", "G"):
                location = Coord(y, x)
                npcs[location] = Creature(c, location, npcs)
        board_str_list[y] = [-2 if c == "#" else 0 for c in line]
    board = np.array(board_str_list, dtype=np.int32)
    paths = {}
    # build_paths(board, paths)
    for npc in npcs.values():
        npc.board = board
        # npc.paths = paths
    return board, npcs


def print_board(board, npcs):
    for y, line in enumerate(board):
        line = [(" " if board[y, x] >= -1 else "█") if (y, x) not in npcs else npcs[(y, x)].species
                for x in range(len(line))]
        print("".join(line))


def run_game(board, npcs):
    for npc in npcs.values():
        npc.all_creatures = npcs
    count = 0
    while True:
        # if count != 47:
        #     print_board(board, npcs)
        #     print(f"count: {count} G HP: {[c for c in npcs.values() if c.species == 'G'][0].friendly_hp()}")
        #     print(f"count: {count} E HP: {[c for c in npcs.values() if c.species == 'E'][0].friendly_hp()}")
        for npc_loc in sorted([l for l in npcs]):
            if npc_loc not in npcs:
                continue
            npc = npcs[npc_loc]
            if not npc.take_turn(board):
                print_board(board, npcs)
                print(f"count: {count} friendly_hp: {npc.friendly_hp()} == {npc.friendly_hp() * count}")
                return npc.friendly_hp() * count

        count += 1


def run_part_2(board, npcs):
    elf_attack = 4
    while True:
        tweaked_npcs = copy(npcs)
        for npc_loc in tweaked_npcs:
            npc = tweaked_npcs[npc_loc]
            npc.hp = 200
            npc.loc = npc_loc
            npc.part_2 = True
            if npc.species == "E":
                npc.attack = elf_attack
        try:
            print(run_game(board, tweaked_npcs))
            return
        except P2Exception as e:
            print(e)
            elf_attack += 1
            print(f"New elf attack power: {elf_attack}")



def tests():
    cave, creatures = parse_board(EXAMPLE_DATA)
    assert run_game(cave, creatures) == 27730
    cave, creatures = parse_board(EXAMPLE_DATA4)
    assert run_game(cave, creatures) == 27755
    cave, creatures = parse_board(EXAMPLE_DATA5)
    assert run_game(cave, creatures) == 28944
    cave, creatures = parse_board(EXAMPLE_DATA6)
    assert run_game(cave, creatures) == 18740
    cave, creatures = parse_board(EXAMPLE_DATA2)
    assert run_game(cave, creatures) == 36334
    cave, creatures = parse_board(EXAMPLE_DATA3)
    assert run_game(cave, creatures) == 39514


if __name__ == '__main__':
    # tests()
    cave, creatures = parse_board(DATA)
    print(cave)
    print(creatures.values())
    print(run_game(cave, copy(creatures)))  # 183300
    run_part_2(cave, creatures)  # 40625