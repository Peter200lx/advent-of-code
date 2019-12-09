from pathlib import Path

from processor import Processor


if __name__ == "__main__":
    DATA = Path("day05.input").read_text().strip()
    int_list = [int(i) for i in DATA.split(",")]

    print(Processor(int_list).run([1]))
    print(Processor(int_list).run([5]))
