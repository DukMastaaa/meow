MAGIC_PRIME = 20201227


def parse():
    public_keys = []
    with open("input/q25.txt", "r") as file:
        for line in file:
            line = line.rstrip()
            if line:
                public_keys.append(int(line))
    return public_keys


def hehehe():
    # BRUTE FORCE LET'S GOOOO
    loops = {}
    value = 1
    loops[value] = 0
    for i in range(1, MAGIC_PRIME + 1):
        value *= 7
        value %= MAGIC_PRIME
        loops[value] = i
    return loops


def transform(subject, loop_size):
    value = 1
    for _ in range(loop_size):
        value *= subject
        value %= MAGIC_PRIME
    return value


def part_a(loops):
    door_pub_key, card_pub_key = parse()
    door_loop_size = loops[door_pub_key]
    card_loop_size = loops[card_pub_key]
    encryption_key = transform(door_pub_key, card_loop_size)
    return encryption_key


if __name__ == '__main__':
    brute_force_loops = hehehe()
    print(part_a(brute_force_loops))
