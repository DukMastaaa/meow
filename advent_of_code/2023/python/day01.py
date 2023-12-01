WORDS = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def get_first(s, ignore_words):
    # scan forward
    idx = 0
    while idx < len(s):
        if not ignore_words:
            for i, word in enumerate(WORDS):
                if s[idx:idx+len(word)] == word:
                    return i
        if '0' <= s[idx] <= '9':
            return int(s[idx])
        idx += 1
    return -1


def get_last(s, ignore_words):
    # scan backward
    idx = len(s)
    while idx >= 0:
        if not ignore_words:
            for i, word in enumerate(WORDS):
                if s[idx-len(word):idx] == word:
                    return i
        if '0' <= s[idx-1] <= '9':
            return int(s[idx-1])
        idx -= 1
    return -1


def value(s, ignore_words):
    first = get_first(s, ignore_words)
    last = get_last(s, ignore_words)
    assert first != -1 and last != -1
    return first * 10 + last


if __name__ == "__main__":
    with open("../input/01.txt", "r") as file:
        l = list(map(str.strip, file.readlines()))
    q1 = map(lambda s: value(s, ignore_words=True), l)
    print(sum(q1))
    q2 = map(lambda s: value(s, ignore_words=False), l)
    print(sum(q2))
