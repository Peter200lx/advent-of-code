import re
from pathlib import Path

example_data = """ADVENT contains no markers and decompresses to itself with no changes, resulting in a decompressed length of 6.
A(1x5)BC repeats only the B a total of 5 times, becoming ABBBBBC for a decompressed length of 7.
(3x3)XYZ becomes XYZXYZXYZ for a decompressed length of 9.
A(2x2)BCD(2x2)EFG doubles the BC and EF, becoming ABCBCDEFEFG for a decompressed length of 11.
(6x1)(1x3)A simply becomes (1x3)A - the (1x3) looks like a marker, but because it's within a data section of another marker, it is not treated any differently from the A that comes after it. It has a decompressed length of 6.
X(8x2)(3x3)ABCY becomes X(3x3)ABC(3x3)ABCY (for a decompressed length of 18), because the decompressed data from the (8x2) marker (the (3x3)ABC) is skipped and not processed further."""

re_comp_tag = re.compile(r"\((?P<nchar>[0-9]*)x(?P<rcount>[0-9]*)\)")


def process_compression(raw_str):
    cur_loc = 0
    exp_str = ""
    while cur_loc < len(raw_str):
        tag = re_comp_tag.search(raw_str, pos=cur_loc)
        if tag is None:
            exp_str += raw_str[cur_loc:]
            break
        else:
            tstart, tend = tag.span()
            exp_str += raw_str[cur_loc:tstart]
            cur_loc = tend
            control = tag.groupdict()
            end_loc = cur_loc + int(control["nchar"])
            substr = raw_str[cur_loc:end_loc]
            exp_str += substr * int(control["rcount"])
            cur_loc = end_loc

    return exp_str


def run_example(data):
    files = [line.split()[0] for line in data.split("\n")]
    for file in files:
        expanded = process_compression(file)
        print(f"{expanded} len={len(expanded)}")


def len_adv_compression(raw_str):
    cur_loc = 0
    length = 0
    while cur_loc < len(raw_str):
        tag = re_comp_tag.search(raw_str, pos=cur_loc)
        if tag is None:
            length += len(raw_str[cur_loc:])
            break
        else:
            tstart, tend = tag.span()
            length += tstart - cur_loc
            cur_loc = tend
            control = tag.groupdict()
            end_loc = cur_loc + int(control["nchar"])
            substr = raw_str[cur_loc:end_loc]
            length += len_adv_compression(substr * int(control["rcount"]))
            cur_loc = end_loc

    return length


if __name__ == "__main__":
    DATA = Path("day09.input").read_text().strip()
    # run_example(example_data)
    print(len(process_compression(DATA)))
    print(len_adv_compression(DATA))
