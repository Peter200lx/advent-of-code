from pathlib import Path

INPUT_FILE = Path(__file__).with_suffix(".input")


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()

    list_o_tri = [[int(x) for x in line.split()] for line in DATA.split("\n")]

    num_valid = 0
    for triangle in list_o_tri:
        triangle.sort()
        if triangle[0] + triangle[1] > triangle[2]:
            num_valid += 1

    print(num_valid)

    import numpy

    num_valid = 0

    np_o_tri = numpy.array([[int(x) for x in line.split()] for line in DATA.split("\n")])

    for i in range(0, len(np_o_tri), 3):
        sublist = np_o_tri[i : i + 3]
        # print(sublist)
        for triangle in numpy.transpose(sublist):
            # print(triangle)
            triangle.sort()
            # print(triangle)
            if triangle[0] + triangle[1] > triangle[2]:
                # print('---VALID')
                num_valid += 1

    print(num_valid)
