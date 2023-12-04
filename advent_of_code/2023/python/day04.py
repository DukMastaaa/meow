with open("../input/04.txt", "r") as file:
    l = [s.strip() for s in file.read().strip().split('\n')]
    acc = 0
    matching_number_counts = []
    for line in l:
        winning, mine = line.partition(":")[2].strip().split(" | ")
        winning = [int(s) for s in winning.split(" ") if s != ""]
        mine = [int(s) for s in mine.split(" ") if s != ""]
        assert len(mine) == len(set(mine))
        assert len(winning) == len(set(winning))
        shared = len(set(mine).intersection(set(winning)))
        matching_number_counts.append(shared)
    q1 = sum(map(lambda shared: 2 ** (shared - 1) if shared > 0 else 0, matching_number_counts))
    print(q1)

    # start with 1 of each card
    total_cards = len(l)
    card_counts = [1] * total_cards
    for i in range(len(card_counts)):
        winning = matching_number_counts[i]
        for j in range(i+1, min(i+winning+1, total_cards)):
            card_counts[j] += card_counts[i] * 1
    q2 = sum(card_counts)
    print(q2)
