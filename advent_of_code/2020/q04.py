import re

# parser time

REQUIRED = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}


def part_a():
    count = 0
    fields_for_this_entry = []

    with open("input/q4.txt", "r") as file:
        for line in file:
            line = line.rstrip()
            if not line:
                if set(fields_for_this_entry).issuperset(REQUIRED):
                    count += 1
                fields_for_this_entry = []
            else:
                fields_for_this_entry.extend(
                    [
                        pair.partition(":")[0]
                        for pair in line.split(" ")
                    ]
                )
    return count


# compiled regex
HGT = re.compile(r"^(\d{2,3})(cm|in)$")
HCL = re.compile(r"^#([0-9a-f]{6})$")
ECL = re.compile(r"^(amb|blu|brn|gry|grn|hzl|oth)$")
PID = re.compile(r"^(\d{9})$")


def hgt(val):
    match = HGT.match(val)
    if not match:
        return False
    num, unit = match.groups()
    if unit == "cm":
        return 150 <= int(num) <= 193
    elif unit == "in":
        return 59 <= int(num) <= 76
    else:
        return False


REGEX_MAGIC = {
    "byr": lambda val: 1920 <= int(val) <= 2002 if val.isdigit() else False,
    "iyr": lambda val: 2010 <= int(val) <= 2020 if val.isdigit() else False,
    "eyr": lambda val: 2020 <= int(val) <= 2030 if val.isdigit() else False,
    "hgt": hgt,
    "hcl": lambda val: bool(HCL.match(val)),
    "ecl": lambda val: bool(ECL.match(val)),
    "pid": lambda val: bool(PID.match(val)),
    "cid": lambda val: True
}


def part_b():
    count = 0
    with open("input/q4.txt", "r") as file:
        fields_for_this_entry = {}
        for line in file:
            line = line.rstrip()
            if not line:
                if set(fields_for_this_entry).issuperset(REQUIRED):
                    if all(REGEX_MAGIC[key](val) for key, val in fields_for_this_entry.items()):
                        count += 1
                fields_for_this_entry = {}
            else:
                for pair in line.split(" "):
                    key, _, value = pair.partition(":")
                    fields_for_this_entry[key] = value
    return count


if __name__ == '__main__':
    print(part_a())
    print(part_b())
