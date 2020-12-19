from math import ceil


def get_notes():
    with open("input/q13.txt", "r") as file:
        line = file.readline().rstrip()
        departure_time = int(line)
        line = file.readline().rstrip()
        buses = line.split(",")
    return departure_time, buses


def part_a():
    departure_time, buses = get_notes()
    buses = list(sorted(int(num) for num in buses if num != "x"))
    next_bus_time = {num: ceil(departure_time / num) * num for num in buses}
    time_diff = {num: bus_time - departure_time for num, bus_time in next_bus_time.items()}
    closest_difference = min(time_diff.values())
    # below is very SQL-esque
    closest_num = [bus_num for bus_num in time_diff if time_diff[bus_num] == closest_difference][0]
    return closest_difference * closest_num


def part_b():
    _, buses = get_notes()
    for i in range(len(buses)):
        if buses[i] != "x":
            buses[i] = int(buses[i])
    time_diff_and_buses = [pair for pair in enumerate(buses) if pair[1] != "x"]
    starting_num = time_diff_and_buses[0][1]
    time_diff_and_buses.pop(0)

    multiplier = 100000000000000 // starting_num  # cheeky - using a hint from the question

    while True:
        starting_time = starting_num * multiplier
        if (starting_time + starting_num) % time_diff_and_buses[-1][1] == 0:
            print(starting_time)
            if all((starting_num * multiplier + diff) % num == 0 for diff, num in time_diff_and_buses):
                return starting_time
        multiplier += 1


"""
Equivalent loopy solution for part_a:
    # closest_difference = -1
    # closest_num = None
    # for num, this_bus_time in next_bus_time.items():
    #     if this_bus_time >= departure_time:
    #         this_difference = this_bus_time - departure_time
    #         if closest_difference == -1 or this_difference < closest_difference:
    #             closest_difference = this_difference
    #             closest_num = num
    #             if this_difference == 0:
    #                 break
"""


if __name__ == '__main__':
    # print(part_a())
    print(part_b())
