import re
from pathlib import Path

FILE_DIR = Path(__file__).parent

EYE_COLORS = {"amb", "blu", "brn", "gry", "grn", "hzl", "hcl", "oth"}

FIELDS = {
    "byr": lambda v: 1920 <= int(v) <= 2002,
    "iyr": lambda v: 2010 <= int(v) <= 2020,
    "eyr": lambda v: 2020 <= int(v) <= 2030,
    "hgt": lambda v: v.endswith("cm") and 150 <= int(v[:-2]) <= 193 or v.endswith("in") and 59 <= int(v[:-2]) <= 76,
    "hcl": lambda v: re.match(r"#[0-9a-f]{6}", v),
    "ecl": lambda v: v in EYE_COLORS,
    "pid": lambda v: len(v) == 9 and v.isnumeric(),
    "cid": lambda v: True,
}
REQUIRED_FIELDS = FIELDS.keys() - {"cid"}


def read_passports(lines):
    passports = []
    passport = {}
    count = 0
    for line in lines:
        if ":" in line:
            line_info = {k: v for k, v in (chunk.split(":") for chunk in line.split())}
            passport.update(line_info)
        else:
            if passport:
                if REQUIRED_FIELDS <= passport.keys():
                    count += 1
                passports.append(passport)
                passport = {}
    if passport:
        if REQUIRED_FIELDS <= passport.keys():
            count += 1
        passports.append(passport)
    print(count)
    return passports


def valid_passport(passport):
    if not REQUIRED_FIELDS <= passport.keys():
        return False
    try:
        for k, v in passport.items():
            if not FIELDS[k](v):
                return False
    except ValueError:
        return False
    return True


if __name__ == "__main__":
    DATA = (FILE_DIR / "day04.input").read_text().strip()
    PASSPORTS = read_passports(DATA.split("\n"))
    print(sum(valid_passport(p) for p in PASSPORTS))
