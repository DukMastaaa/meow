from collections import Counter
from itertools import pairwise


def get_input():
    mapping = {}
    with open("../input/14.txt", "r") as file:
        template = file.readline().strip()
        file.readline()
        for line in file:
            adjacents, result = line.strip().split(" -> ")
            mapping[tuple(adjacents)] = result
    return template, mapping


def pair_counts_to_char_counts(pair_counts: Counter[tuple[str, str], str], start_letter: str) -> Counter[str, str]:
    char_counts = Counter()
    char_counts[start_letter] += 1
    for (_, char), count in pair_counts.items():
        char_counts[char] += count
    return char_counts


def general_solution(template: str, mapping: dict[tuple[str, str], str], iterations: int):
    counter = Counter(p for p in pairwise(template))
    for _ in range(iterations):
        pairs_to_add = Counter()
        for pair in counter:
            count = counter[pair]
            if pair in mapping and count > 0:
                counter[pair] = 0
                new_char = mapping[pair]
                pairs_to_add[(pair[0], new_char)] += count
                pairs_to_add[(new_char, pair[1])] += count
        counter += pairs_to_add

    char_counts = pair_counts_to_char_counts(counter, template[0])
    common = char_counts.most_common()
    return common[0][1] - common[-1][1]


if __name__ == "__main__":
    data = get_input()
    print(general_solution(*data, 10))  # q1
    print(general_solution(*data, 40))  # q2


# old code


def q1(template: str, mapping: dict[str, str], iterations: int):
    for _ in range(iterations):
        things_to_insert = []
        for idx, (now, after) in enumerate(pairwise(template)):
            if (pair := now + after) in mapping:
                things_to_insert.append((idx + 1, mapping[pair]))

        new_template = list(template)
        things_to_insert.reverse()
        for idx, result in things_to_insert:
            new_template.insert(idx, result)
        template = "".join(new_template)

    c = Counter(template)
    common = c.most_common()
    most_common_count = common[0][1]
    least_common_count = common[-1][1]
    return most_common_count - least_common_count
