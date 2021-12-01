from typing import List, Tuple, Dict


def parse():
    player_1 = []
    player_2 = []
    switcher = None
    with open("input/q22.txt", "r") as file:
        for line in file:
            line = line.rstrip()
            if line:
                if line == "Player 1:":
                    switcher = player_1
                elif line == "Player 2:":
                    switcher = player_2
                else:
                    switcher.append(int(line))
    return player_1, player_2


def calculate_score(deck):
    return sum((index + 1) * value for index, value in enumerate(reversed(deck)))


def part_a():
    player_1, player_2 = parse()
    while len(player_1) > 0 and len(player_2) > 0:
        player_1_top = player_1[0]
        player_2_top = player_2[0]
        player_1.pop(0)
        player_2.pop(0)
        if player_1_top > player_2_top:
            player_1.extend((player_1_top, player_2_top))
        elif player_2_top > player_1_top:
            player_2.extend((player_2_top, player_1_top))
        else:
            raise ValueError("what")
    winning_player_cards = player_1 if len(player_2) == 0 else player_2
    return calculate_score(winning_player_cards)


def recursive_combat_game(deck1: List, deck2: List, starting_game: bool) -> int:
    previous_rounds_deck_1 = []
    previous_rounds_deck_2 = []
    while len(deck1) > 0 and len(deck2) > 0:
        tup1 = tuple(deck1)
        tup2 = tuple(deck2)

        if tup1 in previous_rounds_deck_1:
            if tup2 in previous_rounds_deck_2:
                return 1  # end this game

        previous_rounds_deck_1.append(tup1)
        previous_rounds_deck_2.append(tup2)

        p1top = deck1[0]
        p2top = deck2[0]
        deck1.pop(0)
        deck2.pop(0)

        if len(deck1) >= p1top and len(deck2) >= p2top:
            winner = recursive_combat_game(list(deck1[:p1top]), list(deck2[:p2top]), False)
        else:
            winner = 1 if p1top > p2top else 2

        if winner == 1:
            deck1.extend((p1top, p2top))
        else:
            deck2.extend((p2top, p1top))

    game_winner = 1 if len(deck2) == 0 else 2
    winning_deck = deck1 if game_winner == 1 else deck2
    if starting_game:
        return calculate_score(winning_deck)
    else:
        return game_winner


def part_b():
    deck1, deck2 = parse()
    score = recursive_combat_game(deck1, deck2, True)
    return score


if __name__ == '__main__':
    print(part_a())
    print(part_b())
