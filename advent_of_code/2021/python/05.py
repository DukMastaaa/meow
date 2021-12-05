import re
from collections import namedtuple, Counter
from typing import Union
from itertools import combinations, chain
from functools import reduce


INPUT_PATTERN = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")

# assume that the largest x or y coordinate given as input
# is 999.
MAX_INPUT_COORD = 999
GRID_LENGTH = MAX_INPUT_COORD + 1


Position = namedtuple("Position", ["x", "y"])
Horizontal = namedtuple("Horizontal", ["y", "x1", "x2"])
Vertical = namedtuple("Vertical", ["x", "y1", "y2"])
Diagonal = namedtuple("Diagonal", ["x1", "y1", "x2", "y2"])
Line = Union[Horizontal, Vertical, Diagonal]



def coords_to_line(x1: int, y1: int, x2: int, y2: int) -> Line:
    if x1 == x2:
        return Vertical(x1, y1, y2)
    elif y1 == y2:
        return Horizontal(y1, x1, x2)
    else:
        return Diagonal(x1, y1, x2, y2)


def get_input() -> tuple[list[Line], list[Line], list[Line]]:
    horizontals = []
    verticals = []
    diagonals = []
    with open("../input/05.txt", "r") as file:
        for input_line in file:
            input_line = input_line.strip()
            x1, x2, y1, y2 = (int(n) for n in INPUT_PATTERN.match(input_line).groups())
            match line := coords_to_line(x1, x2, y1, y2):
                case Horizontal(_):
                    horizontals.append(line)
                case Vertical(_):
                    verticals.append(line)
                case Diagonal(_):
                    diagonals.append(line)
    return horizontals, verticals, diagonals


def pos_to_number(p: Position) -> int:
    return p.y * GRID_LENGTH + p.x


# no overloading functions :(
def horizontal_to_set(h: Horizontal) -> set[int]:
    initial = pos_to_number(Position(h.x1, h.y))
    final = pos_to_number(Position(h.x2, h.y))
    return set(
        range(min(initial, final), max(initial, final) + 1)
    )


def vertical_to_set(v: Vertical) -> set[int]:
    initial = pos_to_number(Position(v.x, v.y1))
    final = pos_to_number(Position(v.x, v.y2))
    return set(
        range(min(initial, final), max(initial, final) + 1, GRID_LENGTH)
    )


def diagonal_to_set(d: Diagonal) -> set[int]:
    initial = pos_to_number(Position(d.x1, d.y1))
    final = pos_to_number(Position(d.x2, d.y2))
    
    first = min(initial, final)
    second = max(initial, final)
    
    # (first, second) must then define either SW or SE direction.
    # this changes range argument, i'm guessing...
    line_in_se_direction = second % GRID_LENGTH > first % GRID_LENGTH
    return set(
        range(
            first,
            second + 1,
            GRID_LENGTH + 1 if line_in_se_direction else GRID_LENGTH - 1
        )
    )


def q1(data):
    horizontals, verticals, _ = data
    h_sets = [horizontal_to_set(h) for h in horizontals]
    v_sets = [vertical_to_set(v) for v in verticals]
    counter = Counter()

    # compare within h and v, separately
    for set1, set2 in chain(combinations(h_sets, 2), combinations(v_sets, 2)):
        intersection = set1.intersection(set2)
        counter.update(intersection)

    # union h and v separately
    union_h = reduce(set.union, h_sets)
    union_v = reduce(set.union, v_sets)

    # intersect h and v together, count elements???????????
    # this should work because no diagonal lines, so lines are constrained
    whole_intersection = union_h.intersection(union_v)
    counter.update(whole_intersection)

    return sum(counter[e] >= 1 for e in counter)


def q2(data):
    horizontals, verticals, diagonals = data
    h_sets = [horizontal_to_set(h) for h in horizontals]
    v_sets = [vertical_to_set(v) for v in verticals]
    d_sets = [diagonal_to_set(d) for d in diagonals]
    counter = Counter()

    # compare within h, v, d, separately
    for set1, set2 in chain(combinations(h_sets, 2), combinations(v_sets, 2), combinations(d_sets, 2)):
        intersection = set1.intersection(set2)
        counter.update(intersection)

    # union h, v, d separately
    union_h = reduce(set.union, h_sets)
    union_v = reduce(set.union, v_sets)
    union_d = reduce(set.union, d_sets)

    # intersect h and v together, count elements???????????
    # this should work because no diagonal lines, so lines are constrained
    whole_intersection = union_h.intersection(union_v)
    counter.update(whole_intersection)

    return sum(counter[e] >= 1 for e in counter)



if __name__ == "__main__":
    q1data = get_input()
    # q2data = get_input()
    print(q1(q1data))
