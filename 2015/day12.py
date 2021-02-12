import json
import re
from pathlib import Path
from typing import Union

INPUT_FILE = Path(__file__).with_suffix(".input")

RE_NUMS = re.compile(r"-?\d+")


def sum_obj_rec(obj: Union[list, dict]):
    if isinstance(obj, dict):
        if "red" in obj.values():
            return 0
        native = sum(v for v in obj.values() if isinstance(v, (int, float)))
        sub = sum(sum_obj_rec(v) for v in obj.values() if isinstance(v, (list, dict)))
        return native + sub
    else:
        native = sum(v for v in obj if isinstance(v, (int, float)))
        sub = sum(sum_obj_rec(v) for v in obj if isinstance(v, (list, dict)))
        return native + sub


if __name__ == "__main__":
    DATA = INPUT_FILE.read_text().strip()
    print(sum(map(int, RE_NUMS.findall(DATA))))
    print(sum_obj_rec(json.loads(DATA)))
