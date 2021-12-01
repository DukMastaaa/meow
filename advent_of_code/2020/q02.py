import re


# (lower)-(upper) (char): (password)
pattern = re.compile(r"(\d+)-(\d+) (\w): (\w+)")


def part_a():
    count = 0
    with open('input/q2.txt', 'r') as file:
        for line in file:
            match = pattern.match(line)
            lower, upper, char, password = match.groups()
            freq = password.count(char)
            if int(lower) <= freq <= int(upper):
                count += 1
    return count


def part_b():
    count = 0
    with open('input/q2.txt', 'r') as file:
        for line in file:
            match = pattern.match(line)
            lower, upper, char, password = match.groups()
            lower = int(lower) - 1
            upper = int(upper) - 1
            lower_letter = password[lower] == char
            upper_letter = password[upper] == char
            if lower_letter ^ upper_letter:
                count += 1
    return count


if __name__ == '__main__':
    print(part_b())
