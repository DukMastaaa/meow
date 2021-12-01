ALPHA = "abcdefghijklmnopqrstuvwxyz"


def one_group_any(group_answers):
    answers = set()
    for person in group_answers:
        for char in person:
            answers.add(char)
    return list(answers)


def one_group_all(group_answers):
    questions = set(ALPHA)
    difference = set()
    for person in group_answers:
        for char in questions:
            if char not in person:
                difference.add(char)
    questions.difference_update(difference)
    return questions


def solve(comparison_function):
    count = 0
    with open("input/q6.txt", "r") as file:
        group_answers = []
        for line in file:
            line = line.rstrip()
            if not line:
                count += len(comparison_function(group_answers))
                group_answers = []
            else:
                group_answers.append(line)
    return count


def part_a(): return solve(one_group_any)


def part_b(): return solve(one_group_all)


if __name__ == '__main__':
    print(part_a())
    print(part_b())
