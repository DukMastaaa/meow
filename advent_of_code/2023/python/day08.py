import itertools
from math import lcm
from typing import Callable


def parse() -> tuple[str, dict[str, tuple[str, str]]]:
    with open("../input/08.txt", "r") as file:
        l = [s.strip() for s in file.read().strip().split('\n')]
    instructions = l[0]
    network = {}
    for line in l[2:]:
        source, target_tuple = line.split(" = ")
        left, right = target_tuple[1:-1].split(", ")
        network[source] = (left, right)
    return instructions, network


def order_of_single_cycle(start: str, condition: Callable,
                          instructions: str,
                          network: dict[str, tuple[str, str]]) -> int:
    pos = start
    for i, c in enumerate(itertools.cycle(instructions)):
        if condition(pos):
            return i
        pos = network[pos][1 if c == "R" else 0]
    return -1


def q1(instructions: str, network: dict[str, tuple[str, str]]) -> int:
    return order_of_single_cycle(
        "AAA", lambda s: s == "ZZZ", instructions, network
    )


def q2(instructions: str, network: dict[str, tuple[str, str]]) -> int:
    return lcm(*map(
        lambda start: order_of_single_cycle(
            start, lambda s: s.endswith("Z"), instructions, network
        ),
        filter(lambda s: s.endswith("A"), network.keys())
    ))


if __name__ == "__main__":
    instructions, network = parse()
    print(q1(instructions, network))
    print(q2(instructions, network))
