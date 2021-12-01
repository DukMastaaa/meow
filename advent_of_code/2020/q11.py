from typing import List


FLOOR = "."
EMPTY = "L"
OCCUPIED = "#"
SWITCH = {EMPTY: OCCUPIED, OCCUPIED: EMPTY}
DIRECTIONS = {  # (y, x)
    "RIGHT": (0, 1),
    "LEFT": (0, -1),
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "UP-RIGHT": (-1, 1),
    "UP-LEFT": (-1, -1),
    "DOWN-RIGHT": (1, 1),
    "DOWN-LEFT": (1, -1)
}


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

    def count_occupied_neighbours_near(self, pos):
        count = 0
        for direction in DIRECTIONS:
            neighbour = self.pos_in_direction(pos, direction)
            if neighbour is not None:
                if self.at(*neighbour) == OCCUPIED:
                    count += 1
        return count

    def look_in_direction(self, original_pos, direction) -> bool:
        """returns whether there's an occupied seat when looking in `direction`"""
        row, col = original_pos
        add_y, add_x = DIRECTIONS[direction]
        while 0 <= row < self.height and 0 <= col < self.width:
            if self.at(row, col) == OCCUPIED and not (row, col) == original_pos:
                return True
            elif self.at(row, col) == EMPTY and not (row, col) == original_pos:
                return False
            row += add_y
            col += add_x
        return False

    def count_occupied_neighbours_far(self, pos):
        count = 0
        for direction in DIRECTIONS:
            if self.look_in_direction(pos, direction):
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


def change_grid_to_occupied(grid) -> None:
    """optimises things a bit"""
    for i in range(grid.height):
        for j in range(grid.width):
            if grid.at(i, j) == EMPTY:
                grid.grid[i][j] = OCCUPIED


def solve(part: str):
    """part: "a" or "b"."""
    grid = Grid(get_grid())
    change_grid_to_occupied(grid)
    changed_positions = []
    if part == "a":
        adjacent_threshold = 4
        count_function = grid.count_occupied_neighbours_near
    elif part == "b":
        adjacent_threshold = 5
        count_function = grid.count_occupied_neighbours_far
    else:
        return "what"

    while True:
        for i in range(grid.height):
            for j in range(grid.width):
                char = grid.at(i, j)
                if char == FLOOR:
                    continue
                count_calculated = count_function((i, j))
                if char == EMPTY and count_calculated == 0:
                    changed_positions.append((i, j))
                elif char == OCCUPIED and count_calculated >= adjacent_threshold:
                    changed_positions.append((i, j))
        if changed_positions:
            for pos in changed_positions:
                char = grid.at(*pos)
                grid.grid[pos[0]][pos[1]] = SWITCH[char]
            changed_positions.clear()
        else:
            break
    return sum(grid.at(i, j) == OCCUPIED for i in range(grid.height) for j in range(grid.width))


if __name__ == '__main__':
    print(solve('a'))
    print(solve('b'))
