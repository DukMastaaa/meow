import re
from typing import Dict, Optional, Set, List, Tuple

TARGET = "shiny gold"
BAG_PATTERN_WHOLE = re.compile(r"^(.+) bags contain (.+)\.$")
BAG_PATTERN_RIGHT = re.compile(r"(\d) (\w+.\w+) bags?")


def part_a_parser() -> Dict[Optional[str], Set[str]]:
    contained = {}
    with open("input/q7.txt", "r") as file:
        for line in file:
            line = line.rstrip()
            if line:
                outer_bag_name, beans = BAG_PATTERN_WHOLE.match(line).groups()
                if beans == "no other bags":
                    # surely there's a builtin dict method which does this for me
                    try:
                        contained[None].add(outer_bag_name)
                    except KeyError:
                        contained[None] = {outer_bag_name}
                else:
                    matches = BAG_PATTERN_RIGHT.findall(beans)
                    for count, contained_bag_name in matches:
                        try:
                            contained[contained_bag_name].add(outer_bag_name)
                        except KeyError:
                            contained[contained_bag_name] = {outer_bag_name}
    return contained


def part_a_algorithm(contained: Dict[Optional[str], Set[str]]) -> Set[str]:
    # remove empty bags and everything to do with them
    try:
        empty_bags = contained[None]
        for bag in empty_bags:
            del contained[bag]
        del contained[None]
    except KeyError:
        pass

    # confirm bags which target can be in
    confirmed = set()
    for bag in contained[TARGET]:
        confirmed.add(bag)

    # add new bags iteratively based on confirmed bags
    diff = confirmed.copy()
    while diff:
        confirmed_temp = set()
        for bag in diff:
            try:
                confirmed_temp.update(new_bag for new_bag in contained[bag])
            except KeyError:
                continue
        diff = confirmed_temp.difference(confirmed)
        confirmed.update(confirmed_temp)
    return confirmed


def part_b_parser() -> Dict[str, List[Tuple[int, str]]]:
    contains = {}
    with open("input/q7.txt", "r") as file:
        for line in file:
            line = line.rstrip()
            if line:
                outer_bag_name, beans = BAG_PATTERN_WHOLE.match(line).groups()
                if beans == "no other bags":
                    contains[outer_bag_name] = [(0, "")]
                else:
                    matches = BAG_PATTERN_RIGHT.findall(beans)
                    matches = [(int(num), inner_bag_name) for num, inner_bag_name in matches]
                    contains[outer_bag_name] = matches
    return contains


def part_a():
    contained = part_a_parser()
    confirmed = part_a_algorithm(contained)
    return len(confirmed)


def part_b():
    def part_b_algorithm(bag_name):
        if contains[bag_name][0][0] == 0:
            return 0
        else:
            return sum(
                num + num * part_b_algorithm(inside_bag_name)
                for num, inside_bag_name in contains[bag_name]
            )

    contains = part_b_parser()
    result = part_b_algorithm(TARGET)
    return result


if __name__ == '__main__':
    print(part_a())
    print(part_b())
