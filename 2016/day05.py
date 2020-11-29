from hashlib import md5

example_data = "abc"
data = "uqwqemis"


def calc_digit(door_id, num):
    mystr = str(door_id) + str(num)
    myhash = md5(mystr.encode("utf-8")).hexdigest()
    if myhash.startswith("00000"):
        print(f"{mystr} --hash-> {myhash}")
        return myhash[5]
    return None


code = ""
for i in range(29999999):
    code += calc_digit(data, i) or ""
    if i % 1000000 == 0:
        print(f"{i} currently >{code}<")
    if len(code) >= 8:
        break

print(f"--- Answer is: {code}\n\n")


def calc_digit(door_id, num):
    mystr = str(door_id) + str(num)
    myhash = md5(mystr.encode("utf-8")).hexdigest()
    if myhash.startswith("00000") and myhash[5] in (str(i) for i in range(8)):
        print(f"{mystr} --hash-> {myhash}")
        return int(myhash[5]), myhash[6]
    return None


complex_code = [None for i in range(8)]
for i in range(29999999):
    loc_code = calc_digit(data, i)
    if loc_code is not None and complex_code[loc_code[0]] is None:
        complex_code[loc_code[0]] = loc_code[1]
        if None not in complex_code:
            break
    if i % 1000000 == 0:
        print(f"{i} currently >{complex_code}<")

print(f"--- Answer is: {''.join(complex_code)}")
