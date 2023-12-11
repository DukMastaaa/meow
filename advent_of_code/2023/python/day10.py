import dataclasses
from collections import defaultdict
from enum import Enum
from queue import SimpleQueue
from typing import Union


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
    
DIRS = (Dir.NORTH, Dir.EAST, Dir.SOUTH, Dir.WEST)

MESHING_CHARS = [
    "|LJ", "-LF", "|7F", "-J7"
]


@dataclasses.dataclass
class Tile:
    pos: tuple[int, int] = None  # type: ignore
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
        # print(f"{dir.name}, {(i, j)} {'<->' if backlink else '-->'} {neighbour_pos}")


def pos_in_dir(pos: tuple[int, int], dir: Dir) -> tuple[int, int]:
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


def pos_in_bounds(pos: tuple[int, int], height: int, width: int) -> bool:
    return (0 <= pos[0] < height and 0 <= pos[1] < width)


# with open("advent_of_code/2023/input/10test.txt", "r") as file:
with open("../input/10.txt", "r") as file:
    l = [s.strip() for s in file.read().strip().split('\n')]

d: dict[tuple[int, int], Tile] = {}
for i, line in enumerate(l):
    for j, c in enumerate(line):
        d[(i, j)] = Tile()
        d[(i, j)].pos = (i, j)

height = len(l)
width = len(l[0])

starting_pos = (0, 0)
for i, line in enumerate(l):
    for j, c in enumerate(line):
        NEIGHBOURS = {
            Dir.NORTH: (i-1, j),
            Dir.EAST: (i, j+1),
            Dir.SOUTH: (i+1, j),
            Dir.WEST: (i, j-1),
        }
        for dir in DIRS:
            if c in MESHING_CHARS[dir.value]:
                try:
                    d[(i, j)].connect(d[pos_in_dir((i, j), dir)], dir, l)
                except KeyError:
                    pass
        if c == "S":
            starting_pos = (i, j)


q: SimpleQueue[tuple[tuple[int, int], tuple[int, int], int]] = SimpleQueue()
distances = {}
q.put((starting_pos, starting_pos, 0))
while not q.empty():
    pos, prev, dist = q.get()
    if pos in distances:
        break  # loop found?
    distances[pos] = dist
    for neighbour in d[pos].neighbours:
        if neighbour is not None and neighbour.pos != prev:
            q.put((neighbour.pos, pos, dist+1))

q1 = max(distances.items(), key=lambda t: t[1])
print(q1)



# traverse the loop counterclockwise, then keep looking to the left.
# if you see a tile that isn't a part of the loop, that whole region is inside the loop.
# build up a set of regions (need map from pos to region), then at the end sum the contained tiles

# rather than dealing with direction, can go to top-left tile in the loop then go right from there

assert([len([t for t in d[pos].neighbours if t is not None]) == 2 for pos in distances])
# lexicographic sort lol
top_left_pos = min(distances.keys())
assert d[top_left_pos].neighbours[Dir.EAST.value] is not None


regions: list[set[tuple[int, int]]] = []
pos_to_region: dict[tuple[int, int], set[tuple[int, int]]] = {}


def explore_region(start_pos: tuple[int, int],
                   loop: dict[tuple[int, int], int],
                   pos_to_region: dict[tuple[int, int], set[tuple[int, int]]],
                   regions: list[set[tuple[int, int]]],
                   height: int, width: int):
    if not pos_in_bounds(start_pos, height, width):
        print("out of bounds")
        return
    if start_pos in loop or start_pos in pos_to_region:
        return
    q = []
    q.append((start_pos, start_pos))
    new_region = set()
    while q:
        pos, prev = q.pop()
        if pos in loop:
            continue
        pos_to_region[pos] = new_region
        new_region.add(pos)
        for adjacent_pos in map(lambda dir: pos_in_dir(pos, dir), DIRS):
            if (pos_in_bounds(adjacent_pos, height, width) and adjacent_pos != prev
                    and adjacent_pos not in loop and adjacent_pos not in pos_to_region):
                q.append((adjacent_pos, pos))
    if len(new_region) > 0:
        regions.append(new_region)


explore = lambda pos: explore_region(
    pos, distances, pos_to_region, regions, height, width
)

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
    # we travel clockwise.
    explore(pos_in_dir(curr, next_dir.inside_when_clockwise()))
    explore(pos_in_dir(curr, prev_dir.inside_when_clockwise()))
    # update
    prev = curr
    curr = next
    prev_dir = next_dir

q2 = sum(map(lambda s: len(s), regions))
print(q2)
# print(regions)


TRANSLATOR = {
    "|": "│",
    "-": "─",
    "F": "┌",
    "7": "┐",
    "L": "└",
    "J": "┘",
    "S": "S",
    ".": "."
}


# ss = []    
# for i in range(height):
#     for j in range(width):
#         if (i, j) in distances:
#             ss.append(TRANSLATOR[l[i][j]])
#             # ss.append(".")
#         elif (i, j) in pos_to_region:
#             ss.append("I")
#         else:
#             ss.append("O")
#     ss.append("\n")
# ss.append("\n")


# with open("dump.txt", "wb") as file:
#     file.write("".join(ss).encode('utf8'))
