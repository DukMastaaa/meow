def get_numbers():
    with open(f"input/q15.txt", "r") as file:
        numbers = [int(num) for num in file.readline().rstrip().split(",")]
    return numbers


def solve(turn_limit):
    numbers = get_numbers()
    spoken = {num: [index, None] for index, num in enumerate(numbers)}
    recent_number = numbers[-1]
    for turn in range(len(numbers), turn_limit):  # using 0-based index for turns instead of 1
        history = spoken[recent_number]
        if history[1] is None:
            recent_number = 0
        else:
            recent_number = history[0] - history[1]

        if recent_number not in spoken:
            spoken[recent_number] = [turn, None]
        else:
            # cycle to right
            spoken[recent_number][1] = spoken[recent_number][0]
            spoken[recent_number][0] = turn
    return recent_number


def part_a():
    return solve(2020)


def part_b():
    return solve(30000000)


if __name__ == '__main__':
    print(part_a())
    print(part_b())
