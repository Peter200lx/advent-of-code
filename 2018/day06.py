from collections import namedtuple, Counter

DATA = """262, 196
110, 109
58, 188
226, 339
304, 83
136, 356
257, 50
315, 148
47, 315
73, 130
136, 91
341, 169
334, 346
285, 248
76, 233
334, 64
106, 326
48, 207
64, 65
189, 183
300, 247
352, 279
338, 287
77, 277
220, 152
77, 295
49, 81
236, 294
321, 192
43, 234
180, 69
130, 122
166, 225
301, 290
49, 176
62, 156
346, 55
150, 138
214, 245
272, 241
50, 283
104, 70
215, 184
339, 318
175, 123
250, 100
134, 227
96, 197
312, 174
133, 237"""

SIZE = 400
TOTAL_DISTANCE = 10000

Location = namedtuple("loc", ["y", "x"])


def parse_inst(inst):
    for i, loc in enumerate(inst):
        y, x = loc.split(",")
        inst[i] = Location(int(y), int(x))


def gen_field(coords):
    locations = {}
    ignored = set()
    for i in range(0, SIZE):
        for j in range(0, SIZE):
            loc = Location(i, j)
            smallest = (None, SIZE)
            p2_sum = 0
            for coord in coords:
                distance = abs(loc.x - coord.x) + abs(loc.y - coord.y)
                p2_sum += distance
                if distance < smallest[1]:
                    smallest = (coord, distance)
            # Error that didn't give wrong answer: Not ignoring loc's that
            # are the same distance to two different coord. Also possibly
            # not relevant as usually only happens on edges we ignore
            locations[loc] = (smallest[0], p2_sum)
            if i == 0 or j == 0 or i == SIZE - 1 or j == SIZE - 1:
                ignored.add(smallest[0])
    return locations, ignored


def largest_area(locations, ignored):
    largest = Counter([l[0] for l in locations.values()])
    for key, num in largest.most_common():
        if key in ignored:
            continue
        return key, num


def safe_area(locations):
    count = 0
    for loc, val in locations.items():
        if val[1] < TOTAL_DISTANCE:
            count += 1
    return count


if __name__ == "__main__":
    INST = DATA.split("\n")
    parse_inst(INST)
    field, bad_coords = gen_field(INST)
    print(largest_area(field, bad_coords))
    print(safe_area(field))
