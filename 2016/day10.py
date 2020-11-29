import re
from pathlib import Path
from queue import Queue

from functools import reduce

from operator import mul

example_data = """value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2"""

BOT_REGEX = re.compile(r"bot (\d*) gives low to (bot|output) (\d*) and high to (bot|output) (\d*)")
VALUE_REGEX = re.compile(r"value (\d*) goes to (bot|output) (\d*)")


class Holder(object):
    def __init__(self, id_num: int):
        self.id_num = id_num
        self.contents = list()

    def receive(self, chip: int):
        self.contents.append(chip)

    def __repr__(self):
        return f"Holder({self.id_num}{self.contents})"


class Bot(Holder):
    def __init__(self, *args):
        self.low_target = None
        self.high_target = None
        super(Bot, self).__init__(*args)

    def receive(self, chip: int):
        self.contents.append(chip)
        if len(self.contents) > 1:
            g_active.put(self)

    def setup_inst(self, low_to, high_to):
        self.low_target = low_to
        self.high_target = high_to
        pass

    def run(self):
        assert len(self.contents) == 2
        self.low_target.receive(min(self.contents))
        self.high_target.receive(max(self.contents))
        if 61 in self.contents and 17 in self.contents:
            print(f"Bot ({self.id_num}) has processed {self.contents}")


class Output(Holder):
    pass


g_bots = {}
g_outputs = {}
g_active = Queue()


def get_bot(id: int) -> Bot:
    if id not in g_bots:
        g_bots[id] = Bot(id)
    return g_bots[id]


def get_output(id: int) -> Output:
    if id not in g_outputs:
        g_outputs[id] = Output(id)
    return g_outputs[id]


def get_holder(type: str, id: int) -> Holder:
    if type == "bot":
        return get_bot(id)
    elif type == "output":
        return get_output(id)
    else:
        raise ValueError(f"Unknown type {type}")


def setup_state(input):
    for inst in input:
        if inst.startswith("bot"):
            act_list = BOT_REGEX.findall(inst)[0]
            this = get_bot(int(act_list[0]))
            low = get_holder(act_list[1], int(act_list[2]))
            high = get_holder(act_list[3], int(act_list[4]))
            this.setup_inst(low, high)
        elif inst.startswith("value"):
            act_list = VALUE_REGEX.findall(inst)[0]
            holder = get_holder(act_list[1], int(act_list[2]))
            holder.receive(int(act_list[0]))
        else:
            raise ValueError(f"Unknown instruction: {inst}")


def run_sim():
    while not g_active.empty():
        bot = g_active.get()
        bot.run()


if __name__ == "__main__":
    DATA = Path("day10.input").read_text().strip()
    INSTRUCTIONS = [line for line in DATA.split("\n")]

    setup_state(INSTRUCTIONS)
    run_sim()
    print(reduce(mul, [g_outputs[v].contents[0] for v in g_outputs if v in (0, 1, 2)]))
