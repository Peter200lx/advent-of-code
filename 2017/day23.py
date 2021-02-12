from collections import defaultdict
from queue import Queue
from typing import List, Optional

DATA = """set b 93
set c b
jnz a 2
jnz 1 5
mul b 100
sub b -100000
set c b
sub c -17000
set f 1
set d 2
set e 2
set g d
mul g e
sub g b
jnz g 2
set f 0
sub e -1
set g e
sub g b
jnz g -8
sub d -1
set g d
sub g b
jnz g -13
jnz f 2
sub h -1
set g b
sub g c
jnz g 2
jnz 1 3
sub b -17
jnz 1 -23"""


class PartOneDone(Exception):
    pass


class Deadlock(Exception):
    pass


class Program(object):
    def __init__(self, myid: int, rcv_socket: Queue, send_socket: Queue, inst_list: List[str], debug: bool = True):
        self.registers = defaultdict(int)
        self.registers["p"] = myid
        if not debug:
            self.registers["a"] = 1
        self.rcv_socket = rcv_socket
        self.send_socket = send_socket
        self.inst_list = inst_list
        self.prog_counter = 0
        self.send_count = 0
        self.mul_count = 0

    def get_value(self, reg_or_val: str) -> int:
        try:
            return int(reg_or_val)
        except ValueError:
            return self.registers[reg_or_val]

    def i_snd(self, x_val: str) -> None:
        self.send_socket.put(self.get_value(x_val))
        self.send_count += 1

    def i_set(self, x_val: str, y_val: str) -> None:
        self.registers[x_val] = self.get_value(y_val)

    def i_add(self, x_val: str, y_val: str) -> None:
        self.registers[x_val] += self.get_value(y_val)

    def i_sub(self, x_val: str, y_val: str) -> None:
        self.registers[x_val] -= self.get_value(y_val)

    def i_mul(self, x_val: str, y_val: str) -> None:
        self.registers[x_val] *= self.get_value(y_val)
        self.mul_count += 1

    def i_mod(self, x_val: str, y_val: str) -> None:
        self.registers[x_val] %= self.get_value(y_val)

    def i_rcv(self, x_val: str) -> None:
        if self.rcv_socket is self.send_socket:  # Part 1 has loopback FIFO Queue
            if self.get_value(x_val) != 0:
                raise PartOneDone(f"Part one done with rcv of {self.rcv_socket.get()}")
        else:
            if self.rcv_socket.empty() and self.send_socket.empty():
                self.send_socket.put(None)
                raise Deadlock("Deadlock: tried to rcv while other thread was waiting!")
            response = self.rcv_socket.get()
            if response is None:
                raise Deadlock("Deadlock: waiting in rcv and other thread blocked as well!")
            else:
                self.registers[x_val] = response

    def i_jgz(self, x_val: str, y_val: str) -> Optional[int]:
        if self.get_value(x_val) > 0:
            return self.get_value(y_val)
        else:
            return None

    def i_jnz(self, x_val: str, y_val: str) -> Optional[int]:
        if self.get_value(x_val) != 0:
            return self.get_value(y_val)
        else:
            return None

    def run_insts(self):
        while 0 <= self.prog_counter < len(self.inst_list):
            # print(self.array)
            inst = self.inst_list[self.prog_counter].split()
            # print(inst)
            try:
                result = getattr(self, "i_" + inst[0])(*inst[1:])
            except Deadlock as e:
                print(e)
                return
            if result is not None:
                self.prog_counter += result
            else:
                self.prog_counter += 1


def part_two() -> int:
    h_count = 0
    b = 109300  # 93 * 100 + 100000
    c = b + 17000
    while b <= c:
        found = False
        d = 2
        while d != b:
            # Following three lines are new code replacing commented out code
            if b % d == 0:
                found = True
                break
            # e = 2
            # while e != b:
            #     if d * e == b:
            #         found = True
            #     e += 1
            d += 1
        if found:
            h_count += 1
        b += 17
    return h_count


if __name__ == "__main__":
    patch_asm = False
    if patch_asm:
        from datetime import datetime

        print(datetime.now())
    instructions = [s for s in DATA.split("\n")]
    prog = Program(0, None, None, instructions)
    prog.run_insts()
    print(prog.mul_count)
    if patch_asm:
        print(datetime.now())
    print(part_two())
    if patch_asm:
        print(datetime.now())
        instructions[10] = "set g b"  # This is replacing `set e 2` inmost loop
        instructions[11] = "mod g d"
        instructions[12] = "jnz g 8"  # if b % d != 0: goto 'sub d -1'
        instructions[13] = "jnz 1 12"  # else: goto 'sub h -1'
        prog = Program(0, None, None, instructions, debug=False)
        prog.run_insts()
        print(prog.registers["h"])
        print(datetime.now())
