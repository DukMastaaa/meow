from functools import reduce
from math import ceil, floor, prod, sqrt


def max_min_hold(time: int, dist: int) -> tuple[int, int]:
    # quadratic formula
    return (
        floor((time + sqrt(time**2 - 4*dist)) / 2),
        ceil((time - sqrt(time**2 - 4*dist)) / 2)
    )


def ways_to_win(times: list[int], dists: list[int]) -> int:
    # why do i write code like this
    return prod(
        max - min + 1 for max, min in
        (max_min_hold(time, dist) for time, dist in zip(times, dists))
    )


def combine(l: list[int]) -> int:
    return int("".join(map(str, l)))


with open("../input/06.txt", "r") as file:
    times = [int(s) for s in file.readline().partition(":")[2].strip().split(" ") if s != ""]
    dists = [int(s) for s in file.readline().partition(":")[2].strip().split(" ") if s != ""]


q1 = ways_to_win(times, dists)
q2 = ways_to_win([combine(times)], [combine(dists)])
print(q1, q2)
