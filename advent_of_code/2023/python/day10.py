import dataclasses
from collections import defaultdict
from enum import Enum
from queue import SimpleQueue
from typing import Union

Pos = tuple[int, int]


class Dir(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def opposite(self) -> "Dir":
        match self:
            case Dir.NORTH:
                return Dir.SOUTH
            case Dir.EAST:
                return Dir.WEST
            case Dir.SOUTH:
                return Dir.NORTH
            case Dir.WEST:
                return Dir.EAST
        raise ValueError

    def inside_when_clockwise(self) -> "Dir":
        # returns the direction facing inside
        # when going around a loop clockwise.
        match self:
            case Dir.NORTH:
                return Dir.EAST
            case Dir.EAST:
                return Dir.SOUTH
            case Dir.SOUTH:
                return Dir.WEST
            case Dir.WEST:
                return Dir.NORTH
        raise ValueError


def pos_in_dir(pos: Pos, dir: Dir) -> Pos:
    i, j = pos
    match dir:
        case Dir.NORTH:
            return i-1, j
        case Dir.EAST:
            return i, j+1
        case Dir.SOUTH:
            return i+1, j
        case Dir.WEST:
            return i, j-1


def pos_in_bounds(pos: Pos, height: int, width: int) -> bool:
    return (0 <= pos[0] < height and 0 <= pos[1] < width)


DIRS = (Dir.NORTH, Dir.EAST, Dir.SOUTH, Dir.WEST)

MESHING_CHARS = [
    "|LJ", "-LF", "|7F", "-J7"
]


@dataclasses.dataclass
class Tile:
    pos: Pos
    char: str
    neighbours: list[Union["Tile", None]] = dataclasses.field(
        default_factory=lambda: [None, None, None, None]
    )

    def connect(self, other: "Tile", dir: Dir, l: list[str]):
        self.neighbours[dir.value] = other
        backlink = False
        try:
            other_char = l[other.pos[0]][other.pos[1]]
            if other_char == "S" or other_char in MESHING_CHARS[dir.opposite().value]:
                other.neighbours[dir.opposite().value] = self
                backlink = True
        except IndexError:
            pass


def parse() -> tuple[dict[Pos, Tile], Pos, int, int]:
    with open("../input/10.txt", "r") as file:
        l = [s.strip() for s in file.read().strip().split('\n')]
    d = {(i, j): Tile((i, j), c) for i, line in enumerate(l)
         for j, c in enumerate(line)}
    height = len(l)
    width = len(l[0])
    starting_pos = (0, 0)
    # this constructs the whole graph which i don't need lol
    # oh well i'll keep it in
    for i, line in enumerate(l):
        for j, c in enumerate(line):
            if c == "S":
                starting_pos = (i, j)
                continue
            for dir in DIRS:
                if c in MESHING_CHARS[dir.value]:
                    try:
                        d[(i, j)].connect(d[pos_in_dir((i, j), dir)], dir, l)
                    except KeyError:
                        pass
    return d, starting_pos, height, width


def get_loop(d: dict[Pos, Tile], starting_pos: Pos,
             height: int, width: int) -> dict[Pos, int]:
    # BFS
    q: SimpleQueue[tuple[Pos, Pos, int]] = SimpleQueue()
    distances = {}
    q.put((starting_pos, starting_pos, 0))
    while not q.empty():
        pos, prev, dist = q.get()
        if pos in distances:
            break  # loop found
        distances[pos] = dist
        for neighbour in d[pos].neighbours:
            if neighbour is not None and neighbour.pos != prev:
                q.put((neighbour.pos, pos, dist+1))
    return distances


def explore_region(start_pos: Pos,
                   loop: dict[Pos, int],
                   pos_to_region: dict[Pos, set[Pos]],
                   regions: list[set[Pos]],
                   height: int, width: int):
    if not pos_in_bounds(start_pos, height, width):
        print("out of bounds")
        return
    if start_pos in loop or start_pos in pos_to_region:
        return
    stack = []
    stack.append((start_pos, start_pos))
    new_region = set()
    # DFS
    while stack:
        pos, prev = stack.pop()
        if pos in loop:
            continue
        pos_to_region[pos] = new_region
        new_region.add(pos)
        for adjacent_pos in map(lambda dir: pos_in_dir(pos, dir), DIRS):
            if (pos_in_bounds(adjacent_pos, height, width) and adjacent_pos != prev
                    and adjacent_pos not in loop and adjacent_pos not in pos_to_region):
                stack.append((adjacent_pos, pos))
    if len(new_region) > 0:
        regions.append(new_region)


def find_inner_regions(d: dict[Pos, Tile], loop: dict[Pos, int],
                       height: int, width: int) -> tuple[list[set[Pos]], dict[Pos, set[Pos]]]:
    # assert that no branches come out of loop
    assert ([len([t for t in d[pos].neighbours if t is not None])
            == 2 for pos in loop])
    # lexicographic sort lol
    top_left_pos = min(loop.keys())
    # assert that top left tile goes right
    assert d[top_left_pos].neighbours[Dir.EAST.value] is not None

    # autoformat :sob:
    def explore(pos): return explore_region(
        pos, loop, pos_to_region, regions, height, width
    )
    regions: list[set[Pos]] = []
    pos_to_region: dict[Pos, set[Pos]] = {}

    # initial conditions set up for clockwise traversal from top left tile in loop
    prev = top_left_pos
    prev_dir = Dir.EAST
    curr = d[top_left_pos].neighbours[Dir.EAST.value].pos  # type: ignore
    while curr != top_left_pos:
        next_dir, next = [
            (i, t.pos)
            for i, t in enumerate(d[curr].neighbours)
            if t is not None and t.pos != prev
        ][0]
        next_dir = Dir(next_dir)
        # look inward to the centre of the loop
        explore(pos_in_dir(curr, next_dir.inside_when_clockwise()))
        explore(pos_in_dir(curr, prev_dir.inside_when_clockwise()))
        # update
        prev = curr
        curr = next
        prev_dir = next_dir

    return regions, pos_to_region


def q1(loop: dict[Pos, int]) -> int:
    return max(loop.values())


def q2(regions: list[set[Pos]]) -> int:
    return sum(map(lambda s: len(s), regions))


def visualise_q2(loop: dict[Pos, int], pos_to_region: dict[Pos, set],
                 d: dict[Pos, Tile], height: int, width: int):
    CHAR_TO_UNICODE = {
        "|": "│",
        "-": "─",
        "F": "┌",
        "7": "┐",
        "L": "└",
        "J": "┘",
        "S": "S",
        ".": "."
    }
    ss = []
    for i in range(height):
        for j in range(width):
            if (i, j) in loop:
                ss.append(CHAR_TO_UNICODE[d[(i, j)].char])
            elif (i, j) in pos_to_region:
                ss.append("I")
            else:
                ss.append("O")
        ss.append("\n")
    ss.append("\n")
    with open("dump.txt", "wb") as file:
        file.write("".join(ss).encode('utf8'))


if __name__ == "__main__":
    d, starting_pos, height, width = parse()
    loop = get_loop(d, starting_pos, height, width)
    regions, pos_to_region = find_inner_regions(d, loop, height, width)
    print(q1(loop))
    print(q2(regions))
    # visualise_q2(loop, pos_to_region, d, height, width)
