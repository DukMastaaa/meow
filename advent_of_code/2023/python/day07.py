from collections import Counter
from enum import Enum


class HandType(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


VALUE_MAP = {c: i for i, c in enumerate("AKQJT98765432"[::-1])}
JOKER_ORIGINAL_VALUE = VALUE_MAP["J"]


def joker_scoring(hand: list[int]) -> list[int]:
    return list(map(
        lambda n: (
            0 if n == JOKER_ORIGINAL_VALUE
            else n + 1 if n < JOKER_ORIGINAL_VALUE
            else n
        ),
        hand
    ))


def hand_type(hand: list[int], jokers_allowed: bool) -> HandType:
    counter = Counter(hand)
    jokers = counter.pop(0, 0) if jokers_allowed else 0
    counts = list(sorted(counter.values(), reverse=True))
    if not counts:
        counts = [0]
    counts[0] += jokers  # so smart! idea from @kait
    if counts[0] == 5:
        return HandType.FIVE_OF_A_KIND
    if counts[0] == 4:
        return HandType.FOUR_OF_A_KIND
    if counts[0] == 3 and counts[1] == 2:
        return HandType.FULL_HOUSE
    if counts[0] == 3 and counts[1] == 1:
        return HandType.THREE_OF_A_KIND
    if counts[0] == 2 and counts[1] == 2:
        return HandType.TWO_PAIR
    if counts[0] == 2 and counts[1] == 1:
        return HandType.ONE_PAIR
    assert all(count == 1 for count in counts)
    return HandType.HIGH_CARD


def parse() -> list[tuple[list[int], int]]:
    data = []
    with open("../input/07.txt", "r") as file:
        for line in file:
            hand_str, bid = line.strip().split(" ")
            hand = [VALUE_MAP[c] for c in hand_str]
            bid = int(bid)
            data.append((hand, bid))
    return data


def total_winnings(data: list[tuple[list[int], int]], jokers_allowed: bool) -> int:
    if jokers_allowed:
        data = [(joker_scoring(hand), bid) for hand, bid in data]
    ranked = list(sorted(
        data,
        # so smart! lexicographic sort on (hand_type, hand) rather than
        # needing custom comparator and functools.cmp_to_key
        # idea from @luna
        key=lambda t: (hand_type(t[0], jokers_allowed).value, t[0])
    ))
    return sum((i+1)*bid for i, (_, bid) in enumerate(ranked))


if __name__ == "__main__":
    data = parse()
    q1 = total_winnings(data, False)
    q2 = total_winnings(data, True)
    print(q1, q2)
