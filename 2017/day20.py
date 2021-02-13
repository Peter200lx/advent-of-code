from typing import List, Tuple
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

EXAMPLE_DATA = """p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>"""
EXAMPLE2_DATA = """p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>"""


def load_data(particle_str: str) -> List[Tuple[Tuple[int, int, int], ...]]:
    part_list = []
    for line in particle_str.split("\n"):
        part = tuple(tuple(int(i) for i in c[3:-1].split(",")) for c in line.split(", "))
        part_list.append(part)
    return part_list


def find_lowest_acc(part_list: List[Tuple[Tuple[int, int, int]]]) -> List[int]:
    lowest_acc = sum(map(abs, part_list[0][2]))
    lowest_list = []
    for i, part in enumerate(part_list):
        man_dist = sum(map(abs, part[2]))
        if man_dist == lowest_acc:
            lowest_list.append(i)
        elif man_dist < lowest_acc:
            lowest_acc = man_dist
            lowest_list = [i]
    return lowest_list


def clear_collisions(part_list: List[Tuple[Tuple[int, int, int]]]):
    coll_dict = {}
    total_deletes = set()
    for i, part in enumerate(part_list):
        if part[0] not in coll_dict:
            coll_dict[part[0]] = i
        else:
            total_deletes.add(i)
            total_deletes.add(coll_dict[part[0]])
    for i in sorted(total_deletes, reverse=True):
        del part_list[i]
    if total_deletes:
        print(len(part_list))


def step_simulation(part_list: List[Tuple[Tuple[int, int, int]]]):
    for i, part in enumerate(part_list):
        new_vel = tuple(sum(j) for j in zip(part[1], part[2]))
        new_pos = tuple(sum(j) for j in zip(part[0], new_vel))
        part_list[i] = new_pos, new_vel, part[2]


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    particles = load_data(DATA)
    lowest_acc_part_index = find_lowest_acc(particles)
    print(lowest_acc_part_index)
    print([particles[i] for i in lowest_acc_part_index])
    print(len(particles))
    for i in range(100):
        step_simulation(particles)
        clear_collisions(particles)
