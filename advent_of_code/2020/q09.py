from itertools import combinations

PREAMBLE_LENGTH = 5


def get_numbers():
    with open("input/q9.txt", "r") as file:
        numbers = [int(line.rstrip()) for line in file if line != "\n"]
    return numbers


def get_combinations(numbers, starting_index):
    preamble = numbers[starting_index:starting_index+PREAMBLE_LENGTH+1]
    return [c[0] + c[1] for c in combinations(preamble, 2)]


def part_a_algorithm(numbers):  # really inefficient solution
    for starting_index in range(len(numbers) - PREAMBLE_LENGTH - 1 - 1):
        comb = get_combinations(numbers, starting_index)
        this_number = numbers[starting_index + PREAMBLE_LENGTH + 1]
        if this_number not in comb:
            return this_number


def part_a_algorithm_better(numbers):  # better
    # this doesn't actually work for some reason...
    assert len(numbers) > PREAMBLE_LENGTH  # surely
    for starting_index in range(len(numbers) - PREAMBLE_LENGTH - 1 - 1):
        pair_found = False
        end_of_preamble_index = starting_index + PREAMBLE_LENGTH
        num_after_preamble = numbers[end_of_preamble_index]
        for iter_index in range(starting_index, end_of_preamble_index):
            iter_num = numbers[iter_index]
            if num_after_preamble >= iter_num:
                diff = num_after_preamble - iter_num
                if diff in numbers[iter_index:end_of_preamble_index]:
                    pair_found = True
                    break
        if not pair_found:
            return num_after_preamble




def part_b_algorithm(numbers, part_a_answer):
    for start_index in range(len(numbers) - 1):
        count = 0
        current_index = start_index
        smallest = numbers[start_index]
        largest = numbers[start_index]

        while count < part_a_answer and current_index < len(numbers) - 1:
            this_number = numbers[current_index]
            if this_number < smallest:
                smallest = this_number
            elif this_number > largest:
                largest = this_number
            count += this_number
            current_index += 1
        if count == part_a_answer:
            return smallest + largest


def part_a():
    numbers = get_numbers()
    return part_a_algorithm(numbers)


def part_a_better():
    numbers = get_numbers()
    return part_a_algorithm_better(numbers)


def part_b():
    numbers = get_numbers()
    part_a_answer = part_a_algorithm(numbers)
    return part_b_algorithm(numbers, part_a_answer)


if __name__ == '__main__':
    print(part_a_better())
    # print(part_b())
