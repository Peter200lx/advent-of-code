from collections import Counter


def part_1(boxes):
    n2 = 0
    n3 = 0
    for box in boxes:
        counts = Counter(box).values()
        if 2 in counts:
            n2 += 1
        if 3 in counts:
            n3 += 1
    return n2 * n3


def part_2(boxes):
    for string in boxes:
        for string2 in boxes:
            mismatch_loc = []
            for i, c in enumerate(string):
                if string2[i] == c:
                    continue
                mismatch_loc.append(i)
            if len(mismatch_loc) == 1:
                return string[:mismatch_loc[0]] + string[mismatch_loc[0] + 1:]


if __name__ == '__main__':
    with open("day02.input", "r") as in_file:
        DATA = in_file.read().strip("\n")

    list_o_boxes = DATA.split("\n")
    print(part_1(list_o_boxes))
    print(part_2(list_o_boxes))
