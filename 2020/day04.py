import re
from pathlib import Path

FILE_DIR = Path(__file__).parent


FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"}
REQUIRED_FIELDS = FIELDS - {"cid"}

EYE_COLORS = {"amb", "blu", "brn", "gry", "grn", "hzl", "hcl", "oth"}


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
        if not 1920 <= int(passport["byr"]) <= 2002:
            return False
        if not 2010 <= int(passport["iyr"]) <= 2020:
            return False
        if not 2020 <= int(passport["eyr"]) <= 2030:
            return False
        hgt = passport["hgt"]
        if hgt.endswith("cm"):
            if not 150 <= int(hgt[:-2]) <= 193:
                return False
        elif hgt.endswith("in"):
            if not 59 <= int(hgt[:-2]) <= 76:
                return False
        else:
            return False
        if not re.match(r"#[0-9a-f]{6}", passport["hcl"]):
            return False
        if passport["ecl"] not in EYE_COLORS:
            return False
        if len(passport["pid"]) != 9:
            return False
        int(passport["pid"])
    except ValueError:
        return False
    return True


if __name__ == "__main__":
    DATA = (FILE_DIR / "day04.input").read_text().strip()
    PASSPORTS = read_passports(DATA.split("\n"))
    print(sum(valid_passport(p) for p in PASSPORTS))
