from itertools import product
from collections import Counter

Position = tuple[int, int]


def get_input() -> dict[Position, int]:
    data = {}
    with open("../input/11.txt", "r") as file:
        for row_idx, row in enumerate(file):
            row = row.strip()
            for col_idx, num in enumerate(row):
                data[(row_idx, col_idx)] = int(num)
    side_length = row_idx + 1
    return data, side_length


def get_neighbours(pos: Position, side_length: int):
    row, col = pos
    return filter(
        lambda pos: all(coord in range(0, side_length) for coord in pos),
        product(range(row-1, row+2), range(col-1, col+2))
    )


def step(data: dict[Position, int], side_length: int) -> int:
    """
    modifies `data` in-place and returns the number of flashes on this step.
    """
    for pos in data:
        data[pos] += 1
    flash_positions = set()
    flash_positions_this_round = set(pos for pos in data if data[pos] > 9)
    flash_count = 0

    while flash_positions_this_round:
        flash_count += len(flash_positions_this_round)
        flash_positions.update(flash_positions_this_round)
        positions_to_update = Counter()

        for pos in flash_positions_this_round:
            positions_to_update.update(
                filter(
                    lambda pos: pos not in flash_positions,
                    get_neighbours(pos, side_length)
                )
            )
        
        for pos in positions_to_update:
            data[pos] += positions_to_update[pos]
        flash_positions_this_round = \
            set(pos for pos in data if data[pos] > 9).difference(flash_positions)
        

    for pos in flash_positions:
        data[pos] = 0

    return flash_count
    

def q1(data: dict[Position, int], side_length: int, iterations: int):
    total_flashes = 0
    for _ in range(iterations):
        total_flashes += step(data, side_length)
    return total_flashes


def q2(data: dict[Position, int], side_length: int):
    flashes_this_time = 0
    time = 0
    while flashes_this_time < side_length * side_length:
        flashes_this_time = step(data, side_length)
        time += 1
    return time
    

if __name__ == "__main__":
    q1data = get_input()
    q2data = get_input()
    print(q1(*q1data, 100))
    print(q2(*q2data))
