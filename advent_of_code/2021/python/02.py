def get_input():
    data = []
    with open("..\\input\\02.txt", "r") as file:
        for line in file:
            if line != "":
                direction, num = line.split(" ")
                data.append((direction, int(num)))
    return data


def q1(data):
    horizontal_position = 0
    depth = 0

    for direction, num in data:
        match direction:
            case "forward":
                horizontal_position += num
            case "down":
                depth += num
            case "up":
                depth -= num
    
    return horizontal_position * depth


def q2(data):
    horizontal_position = 0
    depth = 0
    aim = 0

    for direction, num in data:
        match direction:
            case "down":
                aim += num
            case "up":
                aim -= num
            case "forward":
                horizontal_position += num
                depth += aim * num

    return horizontal_position * depth


if __name__ == "__main__":
    data = get_input()
    print(q1(data))
    print(q2(data))
