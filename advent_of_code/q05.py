# mmmmmmmm

ROWS_UPPER_INIT = 127
COLS_UPPER_INIT = 7
calc_id = lambda row, col: 8 * row + col

FRONT_MAX_ID = calc_id(0, COLS_UPPER_INIT)
BACK_MIN_ID = calc_id(ROWS_UPPER_INIT, 0)


def bin_partition(code, upper_init):
    lower = 0
    upper = upper_init

    for char in code:
        if char in "FL":
            upper = (upper + lower) // 2
        elif char in "BR":
            lower = (upper + lower) // 2 + 1
        else:
            raise ValueError("uhh")
    assert upper == lower
    return upper


def get_ids():
    ids = []
    with open("q5.txt", "r") as file:
        for line in file:
            line = line.rstrip()
            row = bin_partition(line[:7], ROWS_UPPER_INIT)
            col = bin_partition(line[7:], COLS_UPPER_INIT)
            ids.append(calc_id(row, col))
    return ids


def part_a():
    ids = get_ids()
    return max(ids)


def part_b():
    sorted_ids = list(sorted(get_ids()))
    for this_idx in range(len(sorted_ids) - 1):
        this_id = sorted_ids[this_idx]
        next_id = sorted_ids[this_idx + 1]
        if next_id - this_id == 2 and this_id > FRONT_MAX_ID and next_id < BACK_MIN_ID:
            return this_id + 1


if __name__ == '__main__':
    print(part_a())
    print(part_b())
