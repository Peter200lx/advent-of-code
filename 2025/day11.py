from functools import cache
from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")

KEY_NAMES = frozenset({"fft", "dac"})


class Dev:
    name: str
    outputs: list["Dev"]

    def __init__(self, name: str):
        self.name = name
        self.outputs = []

    @cache
    def find(self, final: str, so_far: frozenset[str] = KEY_NAMES):
        if self.name in KEY_NAMES:
            so_far = so_far | {self.name}
        if self.name == final:
            return int(KEY_NAMES == so_far)
        return sum(o.find(final, so_far) for o in self.outputs)


def parse(data: str):
    devices = {}
    for line in data.split("\n"):
        name, others = line.split(": ")
        instance = devices.setdefault(name, Dev(name))
        for other in others.split():
            instance.outputs.append(devices.setdefault(other, Dev(other)))
    return devices


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    REACTOR = parse(DATA)
    print(REACTOR["you"].find("out"))
    print(REACTOR["svr"].find("out", frozenset()))
