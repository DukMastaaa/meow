from itertools import product  # extremely cool


ACTIVE = "#"
INACTIVE = "."


def get_neighbour_indexes(position):
    ranges = [range(coordinate - 1, coordinate + 2) for coordinate in position]
    for new_position in product(*ranges):
        if new_position != position:
            yield new_position


def parse(dim):
    grid = {}
    with open("input/q17.txt", "r") as file:
        for line_index, line in enumerate(file):
            line = line.rstrip()
            if line:
                # just gonna take top-left as origin, doesn't matter
                for char_index, char in enumerate(line):
                    grid[(char_index, line_index) + (0,) * (dim - 2)] = char
    return grid


def solve(dim, cycles):
    grid = parse(dim)
    pos_to_add = set()
    pos_to_turn_active = []
    pos_to_turn_inactive = []

    for _ in range(cycles):
        pos_to_add.clear()
        pos_to_turn_active.clear()
        pos_to_turn_inactive.clear()

        for pos in grid.keys():
            for neighbour in get_neighbour_indexes(pos):
                if neighbour not in grid:
                    pos_to_add.add(neighbour)
        for pos in pos_to_add:
            grid[pos] = INACTIVE

        for pos in grid.keys():
            active_count = 0
            for neighbour in get_neighbour_indexes(pos):
                if neighbour in grid:
                    if grid[neighbour] == ACTIVE:
                        active_count += 1
            if grid[pos] == ACTIVE:
                if active_count < 2 or active_count > 3:
                    pos_to_turn_inactive.append(pos)
            else:  # INACTIVE
                if active_count == 3:
                    pos_to_turn_active.append(pos)

        for pos in pos_to_turn_inactive:
            grid[pos] = INACTIVE
        for pos in pos_to_turn_active:
            grid[pos] = ACTIVE
    return sum(int(grid[pos] == ACTIVE) for pos in grid)


def part_a():
    return solve(3, 6)


def part_b():
    return solve(4, 6)


if __name__ == '__main__':
    print(part_a())
    print(part_b())
