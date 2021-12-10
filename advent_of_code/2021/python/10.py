from functools import reduce


MATCHING_PAIRS = {
    "(": ")", 
    "[": "]", 
    "{": "}", 
    "<": ">" 
}

Q1_SCORES = {
    ")": 3, "]": 57, "}": 1197, ">": 25137
}

Q2_SCORES = {
    ")": 1, "]": 2, "}": 3, ">": 4
}


def get_input():
    with open("../input/10.txt", "r") as file:
        data = [line.strip() for line in file.readlines() if line != ""]
    return data


def q1(data):
    score = 0
    incomplete_openings = []
    for line in data:
        opening_chars = []
        for char in line:
            if char in "([{<":
                opening_chars.append(char)
            else:
                if char == MATCHING_PAIRS[opening_chars[-1]]:
                    opening_chars.pop()
                else:
                    # line is corrupted
                    print(opening_chars, char)
                    score += Q1_SCORES[char]
                    break
        else:
            # line is incomplete, not corrupted
            incomplete_openings.append(opening_chars)
    return incomplete_openings, score


def q2(incomplete_openings):
    completions = [
        list(map(lambda c: MATCHING_PAIRS[c], opening[::-1]))
        for opening in incomplete_openings
    ]
    
    scores = [
        reduce(lambda prev, char: prev * 5 + Q2_SCORES[char], completion, 0)
        for completion in completions
    ]

    scores.sort()
    return scores[len(scores) // 2]


if __name__ == "__main__":
    data = get_input()
    incomplete_openings, q1answer = q1(data)
    print(q1answer)
    print(q2(incomplete_openings))
