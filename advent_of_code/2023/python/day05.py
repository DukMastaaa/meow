import itertools
from dataclasses import dataclass
from typing import Iterable

# monkey-patch itertools.batched for python < 3.12
if not hasattr(itertools, "batched"):
    def batched(iterable, n):
        # https://docs.python.org/3/library/itertools.html#itertools.batched
        # batched('ABCDEFG', 3) --> ABC DEF G
        if n < 1:
            raise ValueError('n must be at least one')
        it = iter(iterable)
        while batch := tuple(itertools.islice(it, n)):
            yield batch
    setattr(itertools, "batched", batched)


def flatten_list(l: list[list] | Iterable) -> list:
    return list(itertools.chain.from_iterable(l))


@dataclass
class Entry:
    dst_start: int
    src_start: int
    len: int


def parse() -> tuple[list[int], list[list[Entry]]]:
    with open("../input/05.txt", "r") as file:
        l = [s.strip() for s in file.read().strip().split('\n')]
    seeds = list(map(int, l[0].partition(":")[2].strip().split(" ")))
    maps = []
    entries = []
    for line in l[2:]:
        if line != "":
            if "map" in line:
                # Sort by end of source range! Required by map_range
                entries.sort(key=lambda entry: entry.src_start + entry.len)
                maps.append(entries)
                entries = []
            else:
                entries.append(Entry(*map(int, line.split(" "))))
    maps.append(entries)  # don't forget the last one... ugh
    return seeds, maps


def image_of_range(entries: list[Entry], range: tuple[int, int]) -> list[tuple[int, int]]:
    """Returns a list of intervals whose union is the image of the input range."""
    a, b = range
    dst_ranges = []
    prev_intersection_end = a
    for entry in entries:
        intersection = (
            max(a, entry.src_start),
            min(b, entry.src_start + entry.len - 1)
        )
        if intersection[0] <= intersection[1]:
            dst_ranges.append((
                entry.dst_start + (intersection[0] - entry.src_start),
                entry.dst_start + (intersection[1] - entry.src_start)
            ))
            if prev_intersection_end <= intersection[0] - 1:
                dst_ranges.append((prev_intersection_end, intersection[0] - 1))
        prev_intersection_end = max(a, intersection[1] + 1)
    
    if prev_intersection_end <= b:
        dst_ranges.append((prev_intersection_end, b))
    
    return dst_ranges


def general_solution(seed_ranges: list[tuple[int, int]], maps: list[list[Entry]]) -> int:
    result_ranges = seed_ranges
    for m in maps:
        result_ranges = flatten_list(
            map(lambda range: image_of_range(m, range), result_ranges)
        )  # this could be a fold
    return min(map(lambda range: range[0], result_ranges))


def q1(seeds: list[int], maps: list[list[Entry]]) -> int:
    return general_solution([(seed, seed) for seed in seeds], maps)


def q2(seeds: list[int], maps: list[list[Entry]]) -> int:
    seed_ranges = list(map(lambda t: (t[0], t[0] + t[1] - 1), itertools.batched(seeds, 2)))
    return general_solution(seed_ranges, maps)


if __name__ == "__main__":
    seeds, maps = parse()
    print(q1(seeds, maps))
    print(q2(seeds, maps))
