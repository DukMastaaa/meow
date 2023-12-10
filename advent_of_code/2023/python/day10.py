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


MESHING_CHARS = [
    "|LJ", "-LF", "|7F", "-J7"
]


@dataclasses.dataclass
class Tile:
    pos: tuple[int, int] = None  # type: ignore
    neighbours: list[Union["Tile", None]] = dataclasses.field(
        default_factory=lambda: [None, None, None, None]
    )
    
    def connect(self, other: "Tile", dir: Dir, l: list[list[str]]):
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


# with open("advent_of_code/2023/input/10test.txt", "r") as file:
with open("../input/10.txt", "r") as file:
    l = [s.strip() for s in file.read().strip().split('\n')]

d = {}
for i, line in enumerate(l):
    for j, c in enumerate(line):
        d[(i, j)] = Tile()
        d[(i, j)].pos = (i, j)

starting_pos = (0, 0)
for i, line in enumerate(l):
    for j, c in enumerate(line):
        NEIGHBOURS = {
            Dir.NORTH: (i-1, j),
            Dir.EAST: (i, j+1),
            Dir.SOUTH: (i+1, j),
            Dir.WEST: (i, j-1),
        }
        for dir, neighbour_pos in NEIGHBOURS.items():
            if c in MESHING_CHARS[dir.value]:
                try:
                    d[(i, j)].connect(d[neighbour_pos], dir, l)
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
    for i, neighbour in enumerate(d[pos].neighbours):
        if neighbour is not None and neighbour.pos != prev:
            q.put((neighbour.pos, pos, dist+1))

q1 = max(distances.items(), key=lambda t: t[1])
print(q1)




