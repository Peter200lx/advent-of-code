import threading
from collections import defaultdict
from queue import Queue, LifoQueue
from typing import List, Optional

DATA = """set i 31
set a 1
mul p 17
jgz p p
mul a 2
add i -1
jgz i -2
add a -1
set i 127
set p 735
mul p 8505
mod p a
mul p 129749
add p 12345
mod p a
set b p
mod b 10000
snd b
add i -1
jgz i -9
jgz a 3
rcv b
jgz b -1
set f 0
set i 126
rcv a
rcv b
set p a
mul p -1
add p b
jgz p 4
snd a
set a b
jgz 1 3
snd b
set f 1
add i -1
jgz i -11
snd a
jgz f -16
jgz a -19"""
EXAMPLE_DATA = """set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""
EXAMPLE2_DATA = """snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d"""


class PartOneDone(Exception):
    pass


class Deadlock(Exception):
    pass


class Program(object):
    def __init__(self, myid: int, rcv_socket: Queue, send_socket: Queue, inst_list: List[str]):
        self.registers = defaultdict(int)
        self.registers['p'] = myid
        self.rcv_socket = rcv_socket
        self.send_socket = send_socket
        self.inst_list = inst_list
        self.prog_counter = 0
        self.send_count = 0

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

    def i_mul(self, x_val: str, y_val: str) -> None:
        self.registers[x_val] *= self.get_value(y_val)

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

    def run_insts(self):
        while 0 <= self.prog_counter < len(self.inst_list):
            # print(self.array)
            inst = self.inst_list[self.prog_counter].split()
            # print(inst)
            try:
                result = getattr(self, 'i_' + inst[0])(*inst[1:])
            except Deadlock as e:
                print(e)
                return
            if result is not None:
                self.prog_counter += result
            else:
                self.prog_counter += 1


def part_one(instructions: List[str]) -> str:
    loopback = LifoQueue()
    prog = Program(0, loopback, loopback, instructions)
    try:
        prog.run_insts()
    except PartOneDone as e:
        return str(e)


def part_two(instructions: List[str]) -> str:
    prog0_socket = Queue()
    prog1_socket = Queue()
    prog0 = Program(0, prog1_socket, prog0_socket, instructions)
    prog1 = Program(1, prog0_socket, prog1_socket, instructions)
    t0 = threading.Thread(target=prog0.run_insts)
    t1 = threading.Thread(target=prog1.run_insts)
    t0.start()
    t1.start()
    t0.join()
    t1.join()
    return f"Part two done, Program 1 sent {prog1.send_count} times"


if __name__ == '__main__':
    print(part_one([s for s in DATA.split('\n')]))
    print(part_two([s for s in DATA.split('\n')]))
