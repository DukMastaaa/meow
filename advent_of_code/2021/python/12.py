from collections import defaultdict, Counter

Network = defaultdict[str, list[str]]


def get_input():
    network = defaultdict(lambda: [])
    with open("../input/12.txt", "r") as file:
        for line in file:
            node1, node2 = line.rstrip().split("-")
            network[node1].append(node2)
            network[node2].append(node1)
    return network


def get_possible_moves(network: Network, lowercase_history: Counter, current_node: str, do_q2: bool) -> list[str]:
    possible_moves = []

    match lowercase_history.most_common(1):
        case [(_, c)]:
            highest_count = c
        case _:
            highest_count = 0

    for node in network[current_node]:
        if do_q2:
            condition = node.isupper() or highest_count < 2 or lowercase_history[node] == 0
        else:
            condition = node.isupper() or lowercase_history[node] == 0
        
        if node != "start" and condition:
            possible_moves.append(node)

    return possible_moves


def copy_history(old_history: Counter, next_node: str) -> Counter:
    new_history = old_history.copy()
    if next_node.islower():
        new_history[next_node] += 1
    return new_history


def traverse_network(network: Network, lowercase_history: Counter, current_node: str, do_q2: bool) -> int:
    if current_node == "end":
        return 1

    return sum(
        traverse_network(network, copy_history(lowercase_history, node), node, do_q2)
        for node in get_possible_moves(network, lowercase_history, current_node, do_q2)
    )


def combined_solution(network: Network, do_q2: bool):
    lowercase_history = Counter()
    return traverse_network(network, lowercase_history, "start", do_q2)


if __name__ == "__main__":
    network = get_input()
    print(combined_solution(network, False))  # q1
    print(combined_solution(network, True))   # q2, takes a few seconds
