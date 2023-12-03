import itertools
from functools import reduce
from typing import Iterable


def tuple_to_index(row: int, col: int, height: int, width: int) -> int:
    return row * width + col


def index_to_tuple(index: int, height: int, width: int) -> tuple[int, int]:
    return index // width, index % width


def neighbours(index: int, height: int, width: int) -> list[int]:
    row, col = index_to_tuple(index, height, width)
    row_values = []
    col_values = []
    
    if row != 0:
        row_values.append(row-1)
    if row != height - 1:
        row_values.append(row+1)
    row_values.append(row)
    
    if col != 0:
        col_values.append(col-1)
    if col != width - 1:
        col_values.append(col+1)
    col_values.append(col)
    
    # :rolling_eyes:
    output = list(map(lambda p: tuple_to_index(*p, height, width), itertools.product(row_values, col_values)))
    output.pop()  # this removes the centre coordinate. ugh
    return output


def select(c: list | dict, keys: Iterable) -> Iterable:
    for key in keys:
        yield c[key]


def product(l: Iterable):
    return reduce(lambda x, y: x * y, l)


def main():
    with open("../input/03.txt", "r") as file:
        l = [s.strip() for s in file.read().strip().split('\n')]
    height = len(l)
    width = len(l[0])
    
    numbers = []
    digit_index_to_number_index: dict[int, int] = {}
    symbol_indices = []
    gear_indices = []

    start_col = -1
    for row, line in enumerate(l):      
        for col, char in enumerate(line):
            current_index = tuple_to_index(row, col, height, width)
            if char.isdigit():
                if start_col == -1:
                    start_col = col
            else:
                if start_col != -1:
                    # we broke a string of numbers
                    numbers.append(int(line[start_col:col]))
                    for i in range(start_col, col):
                        digit_index_to_number_index[tuple_to_index(row, i, height, width)] = len(numbers) - 1
                    start_col = -1
                if char != ".":
                    # symbol
                    symbol_indices.append(current_index)
                    if char == "*":
                        gear_indices.append(current_index)
        col = len(line)
        # duplicated for end of line check. ugh
        if start_col != -1:
            numbers.append(int(line[start_col:col]))
            for i in range(start_col, col):
                digit_index_to_number_index[tuple_to_index(row, i, height, width)] = len(numbers) - 1
            start_col = -1
    
    # now find which numbers are adjacent to each symbol
    symbol_index_to_adjacent_number_indices: dict[int, set[int]] = {}
    for symbol_index in symbol_indices:
        for neighbour_index in neighbours(symbol_index, height, width):
            if neighbour_index in digit_index_to_number_index.keys():
                symbol_index_to_adjacent_number_indices.setdefault(
                    symbol_index,
                    set()
                ).add(
                    digit_index_to_number_index[neighbour_index]
                )
    
    # collate all numbers then sum
    part_number_indices = reduce(set.union, symbol_index_to_adjacent_number_indices.values())
    q1 = sum(select(numbers, part_number_indices))
    
    # "bad style"
    # this would be so much nicer if i could write as a pipeline
    q2 = sum(
        map(
            lambda set: product(select(numbers, set)),
            filter(
                lambda set: len(set) == 2,
                select(symbol_index_to_adjacent_number_indices, gear_indices)
            )
        )
    )
    
    return q1, q2


if __name__ == "__main__":
    print(main())
