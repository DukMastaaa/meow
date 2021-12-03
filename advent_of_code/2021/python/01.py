from itertools import pairwise


def get_input() -> list[int]:
    with open("..\\input\\01.txt", "r") as file:
        data = [int(line.strip()) for line in file if line != ""]
    return data


def general_solution(data, sliding_window_length: int):
    window_iterators = (data[k:] for k in range(0, sliding_window_length))
    sums_within_windows = (sum(window) for window in zip(*window_iterators))

    count = sum(map(
        lambda pair: pair[1] > pair[0],
        pairwise(sums_within_windows)
    ))

    return count


if __name__ == "__main__":
    data = get_input()
    print(general_solution(data, 1))  # q1
    print(general_solution(data, 3))  # q2


## Older solutions:


def q1_old(data):
    count = 0
    for now, after in pairwise(data):
        if after > now:
            count += 1
    return count


def q2_old(data):
    count = 0
    previous_value = sum(data[0:3])
    for first, second, third in zip(data[0:], data[1:], data[2:]):
        current_value = first + second + third
        if current_value > previous_value:
            count += 1
        previous_value = current_value
    return count
