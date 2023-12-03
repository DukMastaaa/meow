from functools import reduce
import itertools


def neighbours(row: int, col: int, height: int, width: int) -> list[tuple[int, int]]:
    # :rolling_eyes:
    row_values = [row]
    col_values = [col]
    if row != 0:
        row_values.append(row-1)
    if row != height - 1:
        row_values.append(row+1)
    if col != 0:
        col_values.append(col-1)
    if col != width - 1:
        col_values.append(col+1)
    output = list(itertools.product(row_values, col_values))
    output.remove((row, col))  # ugh
    return output


def index_curry(l: list):
    return lambda idx: l[idx]


def tuple_to_index(row: int, col: int, height: int, width: int) -> int:
    return row * width + col


def times(l: set | list):
    prod = 1
    for x in l:
        prod *= x
    return prod


def main():
    with open("../input/03.txt", "r") as file:
        l = [s.strip() for s in file.read().strip().split('\n')]
    height = len(l)
    width = len(l[0])
    
    numbers = []
    coord_mapping = {}
    symbol_coords = []
    gear_coords = []

    acc_number = ""
    stored_coords = []
    for row, line in enumerate(l):
        # duplicated, ugh
        if acc_number != "":
            numbers.append(int(acc_number))
            for coord in stored_coords:
                coord_mapping[coord] = len(numbers) - 1
            acc_number = ""
            stored_coords = []
        
        for col, c in enumerate(line):
            if c.isdigit():
                acc_number += c
                stored_coords.append(tuple_to_index(row, col, height, width))
            else:
                # if we broke an existing string of numbers
                if acc_number != "":
                    numbers.append(int(acc_number))
                    for coord in stored_coords:
                        coord_mapping[coord] = len(numbers) - 1
                    acc_number = ""
                    stored_coords = []
                if c != ".":
                    # symbol
                    symbol_coords.append((row, col))
                    if c == "*":
                        gear_coords.append((row, col))
    
    # now loop through symbols
    part_number_indices = set()

    symbol_to_adjacent_part_number_indices: dict[int, set[int]] = {}
    for row, col in symbol_coords:
        for neighbour_row, neighbour_col in neighbours(row, col, height, width):
            neighbour_hash = tuple_to_index(neighbour_row, neighbour_col, height, width)
            if neighbour_hash in coord_mapping:
                symbol_to_adjacent_part_number_indices.setdefault(
                    tuple_to_index(row, col, height, width),
                    set()
                ).add(
                    coord_mapping[neighbour_hash]
                )
    
    # add the selected numbers
    part_number_indices = set(reduce(set.union, symbol_to_adjacent_part_number_indices.values()))
    q1 = sum(map(index_curry(numbers), part_number_indices))
    
    # to find gears
    gear_ratios_acc = 0
    for row, col in gear_coords:
        gear_hash = tuple_to_index(row, col, height, width)
        # print(list(map(index_curry(numbers), symbol_to_adjacent_part_number_indices[gear_hash])))
        if len(symbol_to_adjacent_part_number_indices[gear_hash]) == 2:
            gear_ratio = reduce(
                lambda x, y: x * y,
                map(index_curry(numbers), symbol_to_adjacent_part_number_indices[gear_hash])
            )
            gear_ratios_acc += gear_ratio
    q2 = gear_ratios_acc
    
    return q1, q2


print(main())
