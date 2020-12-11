from typing import List


FLOOR = "."
EMPTY = "L"
OCCUPIED = "#"
SWITCH = {EMPTY: OCCUPIED, OCCUPIED: EMPTY}
DIRECTIONS = [
    "RIGHT", "LEFT", "UP", "DOWN",
    "UP-RIGHT", "UP-LEFT", "DOWN-RIGHT", "DOWN-LEFT"
]


class Grid(object):
    def __init__(self, grid: List[List[str]]):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])

    def at(self, row, col):
        return self.grid[row][col]

    def pos_in_direction(self, original_pos, direction):
        row, col = original_pos
        if "RIGHT" in direction:
            col += 1
        elif "LEFT" in direction:
            col -= 1
        if "UP" in direction:
            row -= 1
        elif "DOWN" in direction:
            row += 1
        if row < 0 or col < 0 or row >= self.height or col >= self.width:
            return None
        return row, col

    def count_occupied_neighbours(self, pos):
        count = 0
        for direction in DIRECTIONS:
            neighbour = self.pos_in_direction(pos, direction)
            if neighbour is not None:
                if self.at(*neighbour) == OCCUPIED:
                    count += 1
        return count


def get_grid():
    grid = []
    with open("input/q11.txt", "r") as file:
        for line in file:
            line = line.rstrip()
            if line:
                grid.append(list(line))
    return grid


def part_a():
    grid = Grid(get_grid())
    changed_positions = []
    while True:
        for i in range(grid.height):
            for j in range(grid.width):
                char = grid.at(i, j)
                if char == EMPTY and grid.count_occupied_neighbours((i, j)) == 0:
                    changed_positions.append((i, j))
                elif char == OCCUPIED and grid.count_occupied_neighbours((i, j)) >= 4:
                    changed_positions.append((i, j))
        if changed_positions:
            for pos in changed_positions:
                char = grid.at(*pos)
                grid.grid[pos[0]][pos[1]] = SWITCH[char]
            changed_positions.clear()
        else:
            break

    # occupied = 0
    # for i in range(grid.height):
    #     for j in range(grid.width):
    #         if grid.at(i, j) == OCCUPIED:
    #             occupied += 1
    return sum(grid.at(i, j) == OCCUPIED for i in range(grid.height) for j in range(grid.width))


if __name__ == '__main__':
    print(part_a())
