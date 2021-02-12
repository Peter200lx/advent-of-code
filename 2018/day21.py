from day19 import Day19Processor, parse_input

DATA = """#ip 4
seti 123 0 5
bani 5 456 5
eqri 5 72 5
addr 5 4 4
seti 0 0 4
seti 0 9 5
bori 5 65536 3
seti 10828530 0 5
bani 3 255 2
addr 5 2 5
bani 5 16777215 5
muli 5 65899 5
bani 5 16777215 5
gtir 256 3 2
addr 2 4 4
addi 4 1 4
seti 27 4 4
seti 0 4 2
addi 2 1 1
muli 1 256 1
gtrr 1 3 1
addr 1 4 4
addi 4 1 4
seti 25 9 4
addi 2 1 2
seti 17 9 4
setr 2 8 3
seti 7 9 4
eqrr 5 0 2
addr 2 4 4
seti 5 5 4"""


def part_1(instructions):
    proc = Day19Processor(*parse_input(instructions))
    while proc.step_prog():
        # print(proc.prog_counter, proc.registers)
        if proc.prog_counter == 30:
            return proc.registers[5]


def part_2_direct():
    results = set()
    last_result = None
    r5 = 0
    while True:
        r3 = r5 | 65536
        r5 = 10_828_530
        while True:
            r5 += r3 & 255
            r5 &= 16_777_215
            r5 *= 65_899
            r5 &= 16_777_215
            if 256 > r3:
                break
            r3 //= 256

        if r5 not in results:
            results.add(r5)
            # print(r5, bin(r5))
            last_result = r5
        else:
            return last_result


if __name__ == "__main__":
    print(part_1(DATA.split("\n")))
    print(part_2_direct())
