NORTH = "N"
EAST = "E"
WEST = "W"
SOUTH = "S"
LEFT = "L"
RIGHT = "R"
FORWARD = "F"
DIRS = {
    EAST: (1, 0),
    SOUTH: (0, -1),
    WEST: (-1, 0),
    NORTH: (0, 1)
}
CLOCKWISE = list(DIRS.keys())


def get_instructions():
    instructions = []
    with open("input/q12.txt", "r") as file:
        for line in file:
            line = line.rstrip()
            if line:
                instructions.append((line[0], int(line[1:])))
    return instructions


def manhattan(x, y):
    return abs(x) + abs(y)


def part_a():
    instructions = get_instructions()
    x_pos = 0
    y_pos = 0
    direction = 0  # starts east
    for move, number in instructions:
        if move in DIRS:
            delta_x, delta_y = DIRS[move]
            x_pos += delta_x * number
            y_pos += delta_y * number
        elif move == RIGHT:
            direction += number // 90
            direction %= 4
        elif move == LEFT:
            direction -= number // 90
            direction %= 4
        elif move == FORWARD:
            delta_x, delta_y = DIRS[CLOCKWISE[direction]]
            x_pos += delta_x * number
            y_pos += delta_y * number
    return manhattan(x_pos, y_pos)


def rotate_coords(x_pos, y_pos, clockwise: bool, repeat):
    # surely we can do better than this
    for _ in range(repeat):
        temp = x_pos
        x_pos = y_pos
        y_pos = temp
        if clockwise:
            y_pos *= -1
        else:
            x_pos *= -1
    return x_pos, y_pos


def part_b():
    instructions = get_instructions()
    x_pos = 0
    y_pos = 0
    x_way = 10
    y_way = 1
    for move, number in instructions:
        if move in DIRS:
            delta_x, delta_y = DIRS[move]
            x_way += delta_x * number
            y_way += delta_y * number
        elif move == RIGHT or move == LEFT:
            x_way, y_way = rotate_coords(x_way, y_way, move == RIGHT, number // 90)
        elif move == FORWARD:
            x_pos += x_way * number
            y_pos += y_way * number
    return manhattan(x_pos, y_pos)


if __name__ == '__main__':
    print(part_a())
    print(part_b())
