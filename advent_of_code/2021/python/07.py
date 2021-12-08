from math import ceil, floor


def get_input():
    with open("../input/07.txt", "r") as file:
        data = [int(n) for n in file.readline().strip().split(",")]
    return data


def median(data):
    """
    The median minimises the sum of the absolute deviations, i.e.
    median = argmin_{y in R} sum_{i=1}^{n} |x_i - y|.
    """
    data = list(sorted(data))
    l = len(data)
    if l % 2 == 1:
        return data[l // 2]
    else:
        return (data[l // 2] + data[l // 2 + 1]) / 2


def mean(data):
    """
    See ../07part2.png.
    """
    return sum(data) / len(data)


def q1objective(data, y):
    return sum(abs(num - y) for num in data)


def q2objective(data, y):
    return sum(abs(num-y)*(abs(num-y) + 1)/2 for num in data)


def general_solution(data, objective, h_pos_calculator):
    h_pos = h_pos_calculator(data)
    return int(min(
        objective(data, ceil(h_pos)),
        objective(data, floor(h_pos))
    ))


if __name__ == "__main__":
    data = get_input()
    print(general_solution(data, q1objective, median))  # q1
    print(general_solution(data, q2objective, mean))    # q2


# old code


def minimiser(data, objective):
    return min(objective(data, y) for y in range(min(data), max(data) + 1))


def q1old(data):
    return minimiser(data, q1objective)


def q2old(data):
    return minimiser(data, q2objective)
