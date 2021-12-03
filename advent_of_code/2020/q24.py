from typing import Tuple, List

Position = Tuple[int, int]
TRANSLATIONS = {
    "e": (1, 0),
    "w": (-1, 0),
    "ne": (0, 1),
    "nw": (-1, 1),
    "se": (1, -1),
    "sw": (0, -1)
}


def parse_input() -> List[str]:
    moves = []
    with open("input/q24.txt", "r") as file:
        for line in file:
            line = line.rstrip()
            if line:
                moves.append(line)
    return moves


def parse_moves(moves: str):
    index = 0
    x_pos = 0
    y_pos = 0
    while index < len(moves):
        this_char = moves[index]
        if this_char in "ns":
            move = moves[index:index+2]
            index += 1
        else:
            move = this_char
        delta_x, delta_y = TRANSLATIONS[move]
        x_pos += delta_x
        y_pos += delta_y
        index += 1
    return x_pos, y_pos


def get_neighbour_positions(position):
    for delta in TRANSLATIONS.values():
        yield position[0] + delta[0], position[1] + delta[1]


def get_starting_tiles():
    """True is black, False is white"""
    moves = parse_input()
    tiles = {}
    for move in moves:
        pos = parse_moves(move)
        if pos in tiles:
            del tiles[pos]
        else:
            tiles[pos] = True
    return tiles


def part_a():
    return len(get_starting_tiles())


def part_b():
    """very similar to day 17 code"""
    tiles = get_starting_tiles()
    pos_to_add = set()
    pos_to_turn_white = []
    pos_to_turn_black = []

    for _ in range(100):
        pos_to_add.clear()
        pos_to_turn_white.clear()
        pos_to_turn_black.clear()

        for pos in tiles:
            for neighbour in get_neighbour_positions(pos):
                if neighbour not in tiles:
                    pos_to_add.add(neighbour)
        for pos in pos_to_add:
            tiles[pos] = False

        for pos in tiles:
            adjacent_black_tiles = 0
            for neighbour in get_neighbour_positions(pos):
                if neighbour in tiles:
                    if tiles[neighbour] is True:
                        adjacent_black_tiles += 1
            if tiles[pos] is True:  # black tile
                if adjacent_black_tiles == 0 or adjacent_black_tiles > 2:
                    pos_to_turn_white.append(pos)
            else:  # white tile
                if adjacent_black_tiles == 2:
                    pos_to_turn_black.append(pos)

        for pos in pos_to_turn_black:
            tiles[pos] = True
        for pos in pos_to_turn_white:
            tiles[pos] = False
    return sum(int(tiles[pos] is True) for pos in tiles)


if __name__ == '__main__':
    print(part_a())
    print(part_b())
