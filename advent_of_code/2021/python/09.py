Position = tuple[int, int]


def get_input():
    data = {}
    with open("../input/09.txt", "r") as file:
        for row_idx, row in enumerate(file):
            row = row.strip()
            for col_idx, char in enumerate(row):
                data[(row_idx, col_idx)] = int(char)
    return data


def get_neighbours(pos: Position):
    row, col = pos
    return ((row-1, col), (row+1, col), (row, col-1), (row, col+1))


def get_low_points(data: dict[Position, int]):
    pos_to_check = (pos for pos, num in data.items() if num != 9)
    low_points = []
    for pos in pos_to_check:
        this_num = data[pos]
        numbers_around = get_neighbours(pos)
        if all(this_num < data.get(p, 10) for p in numbers_around):
            low_points.append(pos)
    return low_points


def check_pos(pos: Position, pos_already_checked: set[Position], basin_points: set[Position], data: dict[Position, int], side_length: int):
    if pos in pos_already_checked:
        return

    pos_already_checked.add(pos)
    basin_points.add(pos)

    for p in get_neighbours(pos):
        if 0 <= p[0] <= side_length and 0 <= p[1] <= side_length:  # check if p is valid
            check_pos(p, pos_already_checked, basin_points, data, side_length)


def q1(data, low_points):
    return sum(data[pos] + 1 for pos in low_points)


def q2(data, low_points):
    basin_dict = {}
    pos_already_checked = set(pos for pos, num in data.items() if num == 9)
    side_length = max(data)[0]

    for p in low_points:
        basin_points = set()
        check_pos(p, pos_already_checked, basin_points, data, side_length)
        basin_dict[p] = basin_points
    
    basin_sizes = [len(s) for s in basin_dict.values()]
    basin_sizes.sort(reverse=True)
    return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]


if __name__ == "__main__":
    data = get_input()
    low_points = get_low_points(data)
    print(q1(data, low_points))
    print(q2(data, low_points))
