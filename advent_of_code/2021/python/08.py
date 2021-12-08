Pattern = frozenset[str]


def get_input():
    entries = []
    with open("../input/08.txt", "r") as file:
        for line in file:
            line = line.strip()
            uniques, output = line.split(" | ")
            uniques = [frozenset(string) for string in uniques.split(" ")]
            output = [frozenset(string) for string in output.split(" ")]
            entries.append((uniques, output))
    return entries


def q1(data):
    count = 0
    for _, output in data:
        count += sum(len(s) in (2, 3, 4, 7) for s in output)
    return count


def construct_letter_map(uniques: list[Pattern], s_1: Pattern, s_4: Pattern, s_7: Pattern, s_8: Pattern) -> dict[str, str]:
    r"""
    7 \ 1 = a
    4 \ 1 = b, d
    8 \ 4 = a, e, g
    8 \ 7 = b, d, e, g

    counts:
    a = 8  b = 6  c = 8  d = 7
    e = 4  f = 9  g = 7
    """
    a = next(iter(s_7.difference(s_1)))  # gets element in singleton set
    s_8minus4 = s_8.difference(s_4)
    s_8minus7 = s_8.difference(s_7)

    # b, d, e, g, c, f cannot be deduced from 1, 4, 7, 8 alone
    # need to use counting technique
    b, d = s_4.difference(s_1)
    e, g = s_8minus4.intersection(s_8minus7)
    c, f = s_1

    count_for_bd = sum(b in s for s in uniques)
    count_for_eg = sum(e in s for s in uniques)
    count_for_cf = sum(c in s for s in uniques)

    # if counts are not what was expected, switch prospective b <-> d and e <-> g and c <-> f.
    if count_for_bd == 7:
        d, b = b, d
    if count_for_eg == 7:
        g, e = e, g
    if count_for_cf == 9:
        f, c = c, f

    local = locals()
    return {letter: local[letter] for letter in "abcdefg"}  # lol


DEFAULT_SIGNALS_FOR_DIGITS = [
    "abcefg", "cf", "acdeg", "acdfg", "bcdf", "abdfg", "abdefg", "acf", "abcdefg", "abcdfg"
]
PATTERN_TO_DIGIT_TEMPLATE = {p: i for i, p in enumerate(DEFAULT_SIGNALS_FOR_DIGITS)}


def construct_pattern_to_digit_map(uniques: list[frozenset[str]]) -> dict[frozenset[str], int]:
    for s in uniques:
        if len(s) == 2:
            s_1 = s
        elif len(s) == 3:
            s_7 = s
        elif len(s) == 4:
            s_4 = s
    s_8 = frozenset("abcdefg")
    
    letters = construct_letter_map(uniques, s_1, s_4, s_7, s_8)
    pattern_to_digit = {}
    for p, n in PATTERN_TO_DIGIT_TEMPLATE.items():
        pattern_to_digit[frozenset(letters[c] for c in p)] = n

    return pattern_to_digit
    

def q2(data):
    count = 0
    for uniques, output in data:
        pattern_to_digit = construct_pattern_to_digit_map(uniques)
        count += sum(pattern_to_digit[s] * 10 ** (3-i) for i, s in enumerate(output))
    return count


if __name__ == "__main__":
    q1data = get_input()
    q2data = get_input()
    print(q1(q1data))
    print(q2(q2data))
