import re
from collections import defaultdict, namedtuple
from typing import List
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

RE_NUMS = re.compile(r"-?\d+")
Coord = namedtuple("Coord", ["x", "y", "z"])
NanoBot = namedtuple("NanoBot", ["loc", "range"])


def parse_input(instructions: str) -> List[NanoBot]:
    list_o_bots = []
    for line in instructions.split("\n"):
        if line:
            x, y, z, r = tuple(map(int, RE_NUMS.findall(line)))
            list_o_bots.append(NanoBot(Coord(x=x, y=y, z=z), range=r))
    return list_o_bots


def calc_distance(loc1: Coord, loc2: Coord = Coord(0, 0, 0)) -> int:
    return abs(loc1.x - loc2.x) + abs(loc1.y - loc2.y) + abs(loc1.z - loc2.z)


def in_range_of_bot(list_o_bots: List[NanoBot], center_bot: NanoBot) -> List[NanoBot]:
    in_range_bots = []
    for bot in list_o_bots:
        if calc_distance(center_bot.loc, bot.loc) <= center_bot.range:
            in_range_bots.append(bot)
    return in_range_bots


def part_1(list_o_bots: List[NanoBot]) -> int:
    strongest = max(list_o_bots, key=lambda x: x.range)
    return len(in_range_of_bot(list_o_bots, strongest))


def part_2(list_o_bots: List[NanoBot]) -> int:
    bots_sharing_points = defaultdict(set)
    for i, first_bot in enumerate(list_o_bots):
        for second_bot in list_o_bots[i:]:
            if calc_distance(first_bot.loc, second_bot.loc) < first_bot.range + second_bot.range:
                bots_sharing_points[first_bot].add(second_bot)
                bots_sharing_points[second_bot].add(first_bot)

    uniform_connection = False
    while not uniform_connection:
        uniform_connection = None
        least_connected = min(bots_sharing_points, key=lambda x: len(bots_sharing_points[x]))

        for bot in bots_sharing_points[least_connected]:
            if bot != least_connected:
                bots_sharing_points[bot].remove(least_connected)
        del bots_sharing_points[least_connected]

        for bot in bots_sharing_points:
            if uniform_connection is None:
                uniform_connection = len(bots_sharing_points[bot])
            elif uniform_connection != len(bots_sharing_points[bot]):
                uniform_connection = False
                break

    # The following calculation is assuming that we have a bot location close to
    # directly in line with the 0,0,0 location and the answer location. If you can
    # draw a (close-to) straight line from 0,0,0 to the answer and it continues out
    # to a bot, then the answer will be at the bot's distance from 0,0,0 - the bots
    # range. If this "in line" bot exists, then you can find the answer by looking at
    # the maximum value of any bot's distance from 0,0,0 minus that bot's range. This
    # does not hold true universally, such as if all the bots were arranged in a ring
    # on a 2-d plane that is perpendicular to the line from 0,0,0 to the answer.
    # I got the concept for this solution from:
    # https://www.reddit.com/r/adventofcode/comments/a8s17l/2018_day_23_solutions/ecdcqs1/
    # If AoC said I had the wrong answer I was going to transition into a binary
    # search of the points in range of my reduced "bots_sharing_points" cloud. I
    # didn't like the idea of going straight into a binary search of all space as
    # there could have been local maxima that would throw off the binary search.
    # However I figured once I had my space constrained by the list of all bots that
    # share space with each other I believe the gradient would be continuous enough
    # for a binary search to work.
    return max([calc_distance(b.loc) - b.range for b in bots_sharing_points])


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    swarm = parse_input(DATA)
    # print(swarm)
    print(part_1(swarm))
    print(part_2(swarm))
