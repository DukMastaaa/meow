from dataclasses import dataclass
from functools import reduce
import itertools




@dataclass
class MapEntry:
    dest_start: int
    source_start: int
    span: int


class Map:
    def __init__(self, l: list[MapEntry]):
        self.l = l
    
    @classmethod
    def parse(cls, s: str) -> "Map":
        l = []
        for line in s.strip().split("\n"):
            dest_start, source_start, span = map(int, line.split(" "))
            l.append(MapEntry(dest_start, source_start, span))
        l.sort(key=lambda entry: entry.source_start + entry.span)
        return cls(l)
    
    def get(self, source: int) -> int:
        for entry in self.l:
            if 0 <= (diff := source - entry.source_start) < entry.span:
                return entry.dest_start + diff
        return source

    def map_range(self, range: tuple[int, int], hmm: bool) -> list[tuple[int, int]]:
        a, b = range
        output = []
        prev_stop = a
        for entry in self.l:
            intersection = (
                max(a, entry.source_start),
                min(b, entry.source_start + entry.span - 1)
            )
            if intersection[0] <= intersection[1]:
                temp = (
                    entry.dest_start + (intersection[0] - entry.source_start),
                    entry.dest_start + (intersection[1] - entry.source_start)
                )
                output.append(temp)
                if prev_stop <= intersection[0] - 1:
                    temp = (prev_stop, intersection[0] - 1)
                    output.append(temp)
            prev_stop = max(a, intersection[1] + 1)
        
        if prev_stop <= b:
            output.append((prev_stop, b))
        
        if hmm and any(map(lambda t: t[0] == 0, output)):
        # if a == 0:
            print(f"{(a, b)}, {output}")
        return output



def parse():
    # with open("../input/05mytest.txt", "r") as file:
    with open("advent_of_code/2023/input/05.txt", "r") as file:
        l = [s.strip() for s in file.read().strip().split('\n')]
    seeds = list(map(int, l[0].partition(":")[2].strip().split(" ")))
    maps = []
    buf = ""
    for line in l[2:]:
        if line != "":
            if "map" in line:
                if buf != "":
                    maps.append(Map.parse(buf))
                    buf = ""
            else:
                buf += line + "\n"
    maps.append(Map.parse(buf))  # don't forget the last one... ugh
    return seeds, maps


seeds, maps = parse()
print(len(maps))


# part a
locations = []
for seed in seeds:
    result = seed
    # print(result)
    for m in maps:
        result = m.get(result)
        # print(result)
    locations.append(result)
print(min(locations))


# part b
def batched(iterable, n):
    # https://docs.python.org/3/library/itertools.html#itertools.batched
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch

seed_ranges: list[tuple[int, int]] = list(map(lambda t: (t[0], t[0] + t[1] - 1), batched(seeds, 2)))
partb_locations = []
for a, b in seed_ranges:
    print(f"new seed range {(a, b)}")
    result_ranges = [(a, b)]
    # print(result_ranges)
    for i, m in enumerate(maps):
        temp = list(reduce(lambda l1, l2: l1 + l2, list(map(lambda range: m.map_range(range, i == len(maps) - 1), result_ranges))))
        result_ranges = list(set(temp))
        if i == len(maps) - 2:
            print(result_ranges)
    partb_locations.append(min(map(lambda range: range[0], result_ranges)))


print()
print()
print()
print(partb_locations)
print(min(partb_locations))
