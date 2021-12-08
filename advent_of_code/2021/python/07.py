from math import ceil, floor


def get_input():
    with open("../input/07.txt", "r") as file:
        data = [int(n) for n in file.readline().strip().split(",")]
    return data


def q1objective(data, y):
    return sum(abs(num - y) for num in data)


def q1(data):
    """
    The median minimises the sum of the absolute deviations, i.e.
    median = argmin_{y in R} sum_{i=1}^{n} |x_i - y|.
    """
    l = len(data)
    if l % 2 == 1:
        median = data[l // 2]
    else:
        median = (data[l // 2] + data[l // 2 + 1]) / 2
    return q1objective(data, median)


def q2objective(data, y):
    return sum(abs(num-y)*(abs(num-y) + 1)/2 for num in data)


def q2(data):
    """
    See ../07part2.png.
    """
    mean = sum(data) / len(data)
    return min(q2objective(data, floor(mean)), q2objective(data, ceil(mean)))


if __name__ == "__main__":
    data = get_input()
    print(q1(data))
    print(q2(data))


# old code


def minimiser(data, objective):
    return min(objective(data, y) for y in range(min(data), max(data) + 1))


def q1old(data):
    return minimiser(data, q1objective)


def q2old(data):
    return minimiser(data, q2objective)
