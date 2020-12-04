import re
from pathlib import Path

FILE_DIR = Path(__file__).parent


FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"}

REQUIRED_FIELDS = FIELDS - {"cid"}


def read_passports(lines):
    rets = []
    passport = {}
    count = 0
    for line in lines:
        if ":" in line:
            line_info = {chunk.split(":")[0]: chunk.split(":")[1] for chunk in line.split()}
            passport.update(line_info)
        else:
            if passport:
                if all(field in passport for field in REQUIRED_FIELDS):
                    count += 1
                rets.append(passport)
                passport = {}
    if passport:
        if all(field in passport for field in REQUIRED_FIELDS):
            count += 1
        rets.append(passport)
    print(count)
    return rets


def valid_passport(passport):
    if any(field not in passport for field in REQUIRED_FIELDS):
        return False
    try:
        byr = int(passport["byr"])
        if not 1920 <= byr <= 2002:
            return False
        iyr = int(passport["iyr"])
        if not 2010 <= iyr <= 2020:
            return False
        eyr = int(passport["eyr"])
        if not 2020 <= eyr <= 2030:
            return False
        hgt, type = int(passport["hgt"][:-2]), passport["hgt"][-2:]
        if type == "cm":
            if not 150 <= hgt <= 193:
                return False
        elif type == "in":
            if not 59 <= hgt <= 76:
                return False
        else:
            return False
        if not re.match(r"#[0-9a-f]{6}", passport["hcl"]):
            return False
        if passport["ecl"] not in ("amb", "blu", "brn", "gry", "grn", "hzl", "hcl", "oth"):
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
