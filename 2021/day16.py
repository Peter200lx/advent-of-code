from dataclasses import dataclass
from math import prod
from pathlib import Path
from typing import List

INPUT_FILE = Path(__file__).with_suffix(".input")

# fmt: off
HEX_TRANSLATE = {
    "0": "0000", "1": "0001", "2": "0010", "3": "0011",
    "4": "0100", "5": "0101", "6": "0110", "7": "0111",
    "8": "1000", "9": "1001", "A": "1010", "B": "1011",
    "C": "1100", "D": "1101", "E": "1110", "F": "1111",
}
# fmt: on


class Packet:
    version: int
    type: int
    start: int
    end: int

    def sum_ver(self):
        return self.version

    def total(self):
        raise NotImplementedError


@dataclass()
class PacketLiteral(Packet):
    version: int
    type: int
    start: int
    end: int
    value: int

    def total(self):
        return self.value


@dataclass()
class PacketSubPackets(Packet):
    version: int
    type: int
    start: int
    end: int
    subpackets: List[Packet]

    def sum_ver(self):
        return self.version + sum(subp.sum_ver() for subp in self.subpackets)

    def total(self):
        if self.type == 0:
            return sum(subp.total() for subp in self.subpackets)
        elif self.type == 1:
            return prod(subp.total() for subp in self.subpackets)
        elif self.type == 2:
            return min(subp.total() for subp in self.subpackets)
        elif self.type == 3:
            return max(subp.total() for subp in self.subpackets)
        elif self.type == 5:
            assert len(self.subpackets) == 2
            return int(self.subpackets[0].total() > self.subpackets[1].total())
        elif self.type == 6:
            assert len(self.subpackets) == 2
            return int(self.subpackets[0].total() < self.subpackets[1].total())
        elif self.type == 7:
            assert len(self.subpackets) == 2
            return int(self.subpackets[0].total() == self.subpackets[1].total())


def read_packet(binary: str, start: int = 0) -> Packet:
    p_version = int(binary[start : start + 3], 2)
    p_type = int(binary[start + 3 : start + 6], 2)
    if p_type == 4:
        loc = start + 6
        p_value = ""
        while binary[loc] == "1":
            p_value += binary[loc + 1 : loc + 5]
            loc += 5
        p_value += binary[loc + 1 : loc + 5]
        loc += 5
        return PacketLiteral(
            p_version, p_type, start, end=loc, value=int(p_value, 2)
        )
    elif binary[start + 6] == "0":
        subpacket_start = start + 7 + 15
        subpacket_bit_length = int(binary[start + 7 : subpacket_start], 2)
        subpackets = []
        while subpacket_start < start + 7 + 15 + subpacket_bit_length:
            subpacket = read_packet(binary, start=subpacket_start)
            subpacket_start = subpacket.end
            subpackets.append(subpacket)
        return PacketSubPackets(
            p_version, p_type, start, subpackets[-1].end, subpackets
        )
    elif binary[start + 6] == "1":
        subpacket_start = start + 7 + 11
        subpacket_count = int(binary[start + 7 : subpacket_start], 2)
        subpackets = []
        for subpacket_i in range(subpacket_count):
            subpacket = read_packet(binary, start=subpacket_start)
            subpacket_start = subpacket.end
            subpackets.append(subpacket)
        return PacketSubPackets(
            p_version, p_type, start, subpackets[-1].end, subpackets
        )


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    PACKET = read_packet("".join(HEX_TRANSLATE[c] for c in DATA))
    print(PACKET.sum_ver())
    print(PACKET.total())
