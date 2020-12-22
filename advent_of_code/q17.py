ACTIVE = "#"
INACTIVE = "."
SWITCH = {ACTIVE: INACTIVE, INACTIVE: ACTIVE}


def get_neighbour_indexes(position):
    x, y, z = position
    for z_index in range(z - 1, z + 2):
        for y_index in range(y - 1, y + 2):
            for x_index in range(x - 1, x + 2):
                new_position = (x_index, y_index, z_index)
                if new_position != position:
                    yield new_position


def parse():
    grid = {}
    with open("input/q17.txt", "r") as file:
        for line_index, line in enumerate(file):
            line = line.rstrip()
            if line:
                # just gonna take top-left as (0,0,0), doesn't matter
                for char_index, char in enumerate(line):
                    grid[(char_index, line_index, 0)] = char
    return grid


def part_a():
    grid = parse()
    pos_to_change = []
    pos_to_add = []
    for _ in range(6):  # 6 cycles
        pos_to_change.clear()
        pos_to_add.clear()
        for pos in grid.keys():
            active_count = 0
            for neighbour in get_neighbour_indexes(pos):
                if neighbour in grid:
                    if grid[neighbour] == ACTIVE:
                        active_count += 1
                else:
                    pos_to_add.append(neighbour)
            if grid[pos] == ACTIVE:
                if active_count < 2 or active_count > 3:
                    pos_to_change.append(pos)
            else:  # INACTIVE
                if active_count == 3:
                    pos_to_change.append(pos)

        for pos in pos_to_change:
            old_state = grid[pos]
            grid[pos] = SWITCH[old_state]
        for pos in pos_to_add:
            grid[pos] = INACTIVE
    return sum(int(value == ACTIVE) for value in grid.values())


if __name__ == '__main__':
    print(part_a())
