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
    return sum((index + 1) * value for index, value in enumerate(reversed(winning_player_cards)))


if __name__ == '__main__':
    print(part_a())
