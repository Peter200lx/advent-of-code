import heapq
from pathlib import Path
from typing import NamedTuple

import numpy as np
from scipy.optimize import linprog

INPUT_FILE = Path(__file__).with_suffix(".input")


class Machine(NamedTuple):
    indc_goal: tuple[bool, ...]
    buttons: list[set[int]]
    joltage: tuple[int, ...]

    @classmethod
    def from_line(cls, line: str) -> "Machine":
        ind_str, *butt_strs, jolt_str = line.split()
        indc_goal = tuple(bool(c == "#") for c in ind_str.strip("[]"))
        butts = [{int(n) for n in part.strip("()").split(",")} for part in butt_strs]
        jolt = tuple(int(n) for n in jolt_str.strip("{}").split(","))
        return cls(indc_goal, butts, jolt)

    def part1(self) -> int:
        start = 0
        target = sum(1 << i for i, lit in enumerate(self.indc_goal) if lit)
        buttons = [sum(1 << i for i in button) for button in self.buttons]
        queue = [(1, i, start, set()) for i in range(len(self.buttons))]
        heapq.heapify(queue)
        seen = {start: 0}
        while queue:
            cost, next_butt, prev_lights, prev_butts = heapq.heappop(queue)
            next_lights = prev_lights ^ buttons[next_butt]
            if next_lights == target:
                return cost
            if seen.get(next_lights, 999e9) < cost:
                continue
            seen[next_lights] = cost
            prev_butts = prev_butts | {next_butt}
            for i in range(len(buttons)):
                if i in prev_butts:
                    continue
                heapq.heappush(queue, (cost + 1, i, next_lights, prev_butts))

    def part2(self) -> int:
        start = tuple([0] * len(self.joltage))
        queue = [(1, -99e9, i, start) for i in range(len(self.buttons))]
        heapq.heapify(queue)
        seen = {start: 0}
        while queue:
            cost, _dist, next_butt, prev_j = heapq.heappop(queue)
            next_j = tuple(
                j + 1 if i in self.buttons[next_butt] else j
                for i, j in enumerate(prev_j)
            )
            if seen.get(next_j, 999e9) < cost:
                continue
            seen[next_j] = cost
            if next_j == self.joltage:
                print(f"{self=} {cost=}")
                return cost
            if any(j > self.joltage[i] for i, j in enumerate(next_j)):
                # print(f"{cost=} {next_j=} {self.joltage=}")
                continue
            dist = sum(self.joltage[i] - n for i, n in enumerate(next_j))
            for i in range(len(self.buttons)):
                heapq.heappush(queue, (cost + 1, dist, i, next_j))

    def part2_scipy(self) -> int:
        A = np.array(
            [[int(i in b) for b in self.buttons] for i in range(len(self.joltage))]
        )
        b = np.array(self.joltage)
        c = np.ones(len(self.buttons))

        result = linprog(c, A_eq=A, b_eq=b, integrality=c, method="highs")

        if not result.success:
            raise Exception("No solution found")

        presses = np.round(result.x).astype(int)
        total_presses = presses.sum()
        return total_presses


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    MACHINES = [Machine.from_line(line) for line in DATA.split("\n")]

    print(sum(m.part1() for m in MACHINES))
    # print(sum(m.part2() for m in MACHINES))
    print(sum(m.part2_scipy() for m in MACHINES))
