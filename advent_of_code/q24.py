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
    with open("q24.py", "r") as file:
        for line in file:
            line = line.rstrip()
            if line:
                moves.append(line)
    return moves


def parse_moves(moves: str) -> Position:
    index = 0
    x_pos = 0
    y_pos = 0
    while index < len(moves):
        this_char = moves[index]
        if this_char in "ns":
            moves = moves[index:index+2]
            index += 1
        else:
            moves = this_char
        delta_x, delta_y = TRANSLATIONS[moves]
        x_pos += delta_x
        y_pos += delta_y
        index += 1
    return x_pos, y_pos


def part_a():
    moves = parse_input()
    tiles = []
    for move in moves:
        pos = parse_moves(move)
        if pos in tiles:
            tiles.remove(pos)
        else:
            tiles.append(pos)
    
