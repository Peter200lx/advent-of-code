from pathlib import Path
from typing import List

INPUT_FILE = Path(__file__).with_suffix(".input")


def aoc_hash(instr: str) -> int:
    v = 0
    for s in instr:
        v += ord(s)
        v *= 17
        v %= 256
    return v


class Lense:
    def __init__(self, label: str, val: int):
        self.label = label
        self.val = val
        self.prev = None
        self.next = None

    def find(self, label: str):
        if self.label == label:
            return self
        if self.next is not None:
            return self.next.find(label)
        return None

    def pop(self):
        if self.next:
            self.next.prev = self.prev
        if self.prev:
            self.prev.next = self.next

    def plus_next_val(self, depth: int = 1):
        ret = self.val * depth
        if self.next:
            ret += self.next.plus_next_val(depth + 1)
        return ret


class Wall:
    def __init__(self):
        self.boxes = [None] * 256

    def pop_box(self, label: str, loc: int):
        head = self.boxes[loc]
        if head is None:
            return
        lense = head.find(label)
        if lense is None:
            return
        elif lense == head:
            self.boxes[loc] = lense.next
            lense.prev = None
        else:
            lense.pop()

    def add_box(self, label: str, loc: int, val: int):
        head = self.boxes[loc]
        if head is None:
            self.boxes[loc] = Lense(label, val)
            return
        lense = head.find(label)
        if lense:
            lense.val = val
        else:
            cur = head
            while cur.next is not None:
                cur = cur.next
            cur.next = Lense(label, val)
            cur.next.prev = cur

    def run_cmds(self, cmds: List[str]):
        for cmd in cmds:
            if "-" in cmd:
                label = cmd.split("-", maxsplit=1)[0]
                box_id = aoc_hash(label)
                self.pop_box(label, box_id)
            elif "=" in cmd:
                label, val = cmd.split("=", maxsplit=1)
                box_id = aoc_hash(label)
                self.add_box(label, box_id, int(val))
        ret = 0
        for box_num, lense in enumerate(self.boxes, start=1):
            if lense:
                ret += box_num * lense.plus_next_val()
        return ret


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    STRINGS = [s for s in DATA.split(",")]

    print(sum(aoc_hash(s) for s in STRINGS))

    print(Wall().run_cmds(STRINGS))
