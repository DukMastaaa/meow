numbers = []
with open("input/q1.txt", "r") as file:
    for line in file:
        line = line.rstrip()
        if line:
            numbers.append(int(line))
TARGET = 2020


def part_a():
    odd = sorted([num for num in numbers if num % 2 == 1])
    even = sorted([num for num in numbers if num % 2 == 0])
    for parity in odd, even:
        parity_len = len(parity)
        for end_index in range(1, parity_len + 1):
            diff = TARGET - parity[-end_index]
            for pair_index in range(parity_len - end_index):
                if parity[pair_index] == diff:
                    # we found a match!
                    first_num = parity[-end_index]
                    second_num = parity[pair_index]
                    assert first_num + second_num == TARGET
                    return first_num * second_num
    # pog


def part_b():
    # uhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh not efficient at all but sure
    number_len = len(numbers)
    for end_index in range(1, number_len + 1):
        end_num = numbers[-end_index]
        for middle_index in range(end_index, number_len + 1):  # probably a bug here
            middle_num = numbers[-middle_index]
            for start_index in range(middle_index):
                start_num = numbers[start_index]
                total = start_num + middle_num + end_num
                if total == TARGET:
                    return start_num * middle_num * end_num
    return "it doesn't work"


PARITIES = {  # true indicates odd
    (True, True): False,
    (True, False): True,
    (False, True): True,
    (False, False): False
}


def better_part_b():
    # going to adapt part_b with some strategy from get_ids
    number_len = len(numbers)
    triplet = [False, False]
    for end_index in range(1, number_len + 1):
        end_num = numbers[-end_index]
        triplet[0] = end_num % 2 == 1
        for middle_index in range(end_index, number_len + 1):  # probably a bug here
            middle_num = numbers[-middle_index]
            triplet[1] = middle_num % 2 == 1
            for start_index in range(middle_index):
                start_num = numbers[start_index]
                if PARITIES[tuple(triplet)] == (start_num % 2 == 1):  # ignore the TypeError
                    total = start_num + middle_num + end_num
                    if total == TARGET:
                        return start_num * middle_num * end_num


if __name__ == '__main__':
    print(part_a())
    print(better_part_b())