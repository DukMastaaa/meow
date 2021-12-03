def parse():
    with open("input/q23.txt", "r") as file:
        line = file.readline().strip()
    links = {}
    first = int(line[0])
    last = int(line[-1])
    for i in range(len(line)):
        try:
            links[int(line[i])] = int(line[i+1])
        except IndexError:
            links[int(line[i])] = first
    return links, first, last


def algorithm(links, first, total_size, iterations):
    def calculate_dest_cup(index):
        return ((index - 1) - 1) % total_size + 1

    current_cup_num = first
    for _ in range(iterations):
        next_nums = [current_cup_num]
        for i in range(1, 5):
            if next_nums[i-1] not in links:
                links[next_nums[i-1]] = next_nums[i-1] + 1
            next_nums.append(links[next_nums[i-1]])
        next_nums.pop(0)

        dest = calculate_dest_cup(current_cup_num)
        while dest in next_nums[:3]:
            dest = calculate_dest_cup(dest)
        after_dest = links[dest]

        # cycle
        links[current_cup_num] = next_nums[3]
        links[next_nums[2]] = after_dest
        links[dest] = next_nums[0]

        # go clockwise once
        current_cup_num = links[current_cup_num]
    # already alters `links` in place.


def part_a():
    links, first, _ = parse()
    algorithm(links, first, len(links), 100)
    cup_list = [1]
    for _ in range(len(links)):
        cup_list.append(links[cup_list[-1]])
    cup_list.pop()  # there will be a trailing 1 at the end because of links

    one_index = cup_list.index(1)
    list_without_one = cup_list[one_index + 1:] + cup_list[:one_index]
    return "".join(str(num) for num in list_without_one)


def part_b():
    links, first, last = parse()
    starting_count = len(links)
    links[last] = starting_count + 1
    links[1_000_000] = first

    algorithm(links, first, 1_000_000, 10_000_000)
    next1 = links[1]
    next2 = links[next1]
    return next1 * next2


if __name__ == '__main__':
    print(part_a())
    print(part_b())


# def bad_algorithm(cups, iterations):
#     current_cup_index = 0
#     cup_count = len(cups)
#     max_cup = max(cups)
#     min_cup = min(cups)
#
#     for _ in range(iterations):
#         current_cup_label = cups[current_cup_index]
#         removed_cups = []
#
#         for i in range(3):
#             removed_cups.append(cups[(current_cup_index + i + 1) % cup_count])
#         for label in removed_cups:
#             cups.remove(label)
#
#         destination_label = current_cup_label - 1
#         if destination_label < min_cup:
#             destination_label = max_cup
#
#         while destination_label in removed_cups:
#             destination_label -= 1
#             if destination_label < min_cup:
#                 destination_label = max_cup
#
#         destination_index = cups.index(destination_label)
#         for removed_label in reversed(removed_cups):
#             cups.insert(destination_index + 1, removed_label)
#         current_cup_index = cups.index(current_cup_label) + 1
#         current_cup_index %= cup_count
#
#     return cups
