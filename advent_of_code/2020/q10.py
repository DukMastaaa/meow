from functools import lru_cache


def get_adapter_joltages():
    with open("input/q10.txt", "r") as file:
        adapter_joltages = [int(line.rstrip()) for line in file if line != "\n"]
    return list(sorted(adapter_joltages))


def part_a():
    joltages = get_adapter_joltages()
    joltages.insert(0, 0)
    differences = []
    for index in range(len(joltages) - 1):
        differences.append(joltages[index+1] - joltages[index])
    diff_1 = differences.count(1)
    diff_3 = differences.count(3)
    diff_3 += 1
    return diff_1 * diff_3


def part_b():
    @lru_cache()
    def part_b_algorithm(starting_index):
        current_index = starting_index
        while current_index < len(joltages) - 1:
            current_num = joltages[current_index]
            branching_indexes = []
            try:
                for offset in range(1, 4):
                    if joltages[current_index + offset] - current_num <= 3:
                        branching_indexes.append(current_index + offset)
            except IndexError:
                pass
            if len(branching_indexes) == 1:
                current_index = branching_indexes[0]
            else:
                return sum(part_b_algorithm(index) for index in branching_indexes)
        return 1  # path went to the end!

    joltages = get_adapter_joltages()
    joltages.insert(0, 0)
    count = part_b_algorithm(0)
    return count


if __name__ == '__main__':
    print(part_a())
    print(part_b())
