import sys

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
INSTRUCTIONS = [s for s in DATA.split('\n')]

g_array = [0 for _ in range(26)]
g_last_sound = None


def get_index(reg) -> int:
    return ord(reg) - ord('a')


def get_value(reg_or_val) -> int:
    try:
        return int(reg_or_val)
    except ValueError:
        return g_array[get_index(reg_or_val)]


def a_snd(x_val):
    global g_last_sound
    g_last_sound = get_value(x_val)


def a_set(x_val, y_val):
    g_array[get_index(x_val)] = get_value(y_val)


def a_add(x_val, y_val):
    g_array[get_index(x_val)] += get_value(y_val)


def a_mul(x_val, y_val):
    g_array[get_index(x_val)] *= get_value(y_val)


def a_mod(x_val, y_val):
    g_array[get_index(x_val)] %= get_value(y_val)


def a_rcv(x_val):
    if get_value(x_val) > 0:
        print(g_last_sound)
        sys.exit(0)


def a_jgz(x_val, y_val):
    if get_value(x_val) > 0:
        return get_value(y_val)
    else:
        return None


INST_DICT = {
    'snd': a_snd,
    'set': a_set,
    'add': a_add,
    'mul': a_mul,
    'mod': a_mod,
    'rcv': a_rcv,
    'jgz': a_jgz,
}


def run_instructions(instructions: str):
    inst_loc = 0
    while 0 <= inst_loc < len(instructions):
        print(g_array)
        inst = instructions[inst_loc].split(' ')
        print(inst)
        result = INST_DICT[inst[0]](*inst[1:])
        if result is not None:
            inst_loc += result
        else:
            inst_loc += 1





if __name__ == '__main__':
    run_instructions(INSTRUCTIONS)


















