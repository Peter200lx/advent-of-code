from collections import Counter
from math import prod
from pathlib import Path
from typing import List, Dict, Optional, Set

INPUT_FILE = Path(__file__).with_suffix(".input")


START_BOT = "ore"
P1_MINUTES = 24
P2_MINUTES = 32


def req_met(
    req: Dict[str, int], items: Counter[str, int]
) -> Optional[Counter[str, int]]:
    reduced = items.copy()
    for item, cost in req.items():
        reduced[item] -= cost
        if reduced[item] < 0:
            return
    return reduced


class Blueprint:
    def __init__(self, in_str: str):
        id_blob, rest = in_str.split(": ")
        self.id = int(id_blob[-2:])
        self.costs: Dict[str, Dict[str:int]] = {}
        for bot_str in reversed(rest.split(". ")):
            front, cost = bot_str.split(" costs ")
            _each, bot_type, _robot = front.split()
            cost = cost.rstrip(".")
            req_dict = {}
            for req in cost.split(" and "):
                req_num, req_type = req.split()
                req_dict[req_type] = int(req_num)
            self.costs[bot_type] = req_dict

        self.max_want: Dict[str, int] = {}
        for req_dict in self.costs.values():
            for resource, cost in req_dict.items():
                self.max_want[resource] = max(self.max_want.get(resource, 0), cost)

        self.max_filter = self._build_reduced()

    def _build_reduced(self):
        filt = [{}] * (P2_MINUTES + 1)
        filt[0] = {"ore": 0, "clay": 0, "obsidian": 0}
        filt[1] = self.costs["geode"] | {"clay": 0}
        filt[2] = self.max_want.copy()
        for i in range(2, P2_MINUTES):
            filt[i + 1] = {k: v * i for k, v in self.max_want.items()}
        return filt

    def __repr__(self):
        return f"Blueprint({self.id=} {self.costs=})"

    def run_dfs(
        self,
        items: Counter[str, int],
        bots: Counter[str, int],
        ignored: Set[str],
        cache: Optional[dict] = None,
        minutes: int = P1_MINUTES,
    ) -> int:
        if cache is None:
            cache = {}
        if minutes <= 0:
            return 0
        best = 0
        for res, max_val in self.max_filter[minutes].items():
            items[res] = min(items[res], max_val)
        key = (
            "".join(f"{k}{v:x}" for k, v in items.items())
            + "".join(f"{k}{v:x}" for k, v in bots.items()),
            minutes,
        )
        if key in cache:
            return cache[key]
        tried: Set[str] = set()
        for bot, requires in self.costs.items():
            if bot in ignored:
                continue
            if bots[bot] > self.max_want.get(bot, 9999999999):
                continue
            try_buy = req_met(requires, items)
            if try_buy is None:
                continue
            new_bots = bots + Counter((bot,))
            best = max(
                best, self.run_dfs(try_buy + bots, new_bots, set(), cache, minutes - 1)
            )
            tried.add(bot)
            if bot == "geode":
                break
        best = max(
            best, self.run_dfs(items + bots, bots, ignored | tried, cache, minutes - 1)
        )
        cache[key] = best + bots["geode"]
        return cache[key]


def part_1(blueprints: List[Blueprint]) -> int:
    results = {
        b.id: b.run_dfs(Counter(), Counter((START_BOT,)), set()) for b in blueprints
    }
    print(results)
    return sum(i * c for i, c in results.items())


def part_2(blueprints: List[Blueprint]) -> int:
    blueprints = blueprints[:3]
    results = {}
    for b in blueprints:
        results[b.id] = b.run_dfs(
            Counter(), Counter((START_BOT,)), set(), minutes=P2_MINUTES
        )
        print(results)
    return prod(c for c in results.values())


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    BLUEPRINTS = [Blueprint(line) for line in DATA.split("\n")]

    print(part_1(BLUEPRINTS))
    print(part_2(BLUEPRINTS))
