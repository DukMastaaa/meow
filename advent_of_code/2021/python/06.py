from collections import Counter

def get_input():
    with open("../input/06.txt", "r") as file:
        data = [int(num) for num in file.readline().strip().split(",")]
    return data


def general_solution(data, iterations: int):
    c = Counter()
    c.update(data)

    for _ in range(iterations):
        add_6s_and_8s_from_0 = c[0]
        for i in range(1, 9):
            c[i-1] = c[i]
        c[8] = add_6s_and_8s_from_0
        c[6] += add_6s_and_8s_from_0

    return c.total()

if __name__ == "__main__":
    q1data = get_input()
    print(general_solution(q1data, 256))


# old code


DEFAULT_LIFETIME = 6


def q1old(data):
    data = [(n, DEFAULT_LIFETIME) for n in data]
    for _ in range(80):
        # print(",".join(list(str(t[0]) for t in data)))
        indices_to_reduce = []  # contains index
        fishes_to_reset = []    # contains index
        fishes_born_today = []  # contains new lifetime
        for index, fish in enumerate(data):
            age, lifetime = fish
            if age > 0:
                indices_to_reduce.append(index)
            else:
                fishes_born_today.append(DEFAULT_LIFETIME + 2)
                fishes_to_reset.append(index)
        
        for index in indices_to_reduce:
            old_age, _ = data[index]
            data[index] = (old_age - 1, DEFAULT_LIFETIME)
        
        for index in fishes_to_reset:
            # _, lifetime = data[index]
            # data[index] = (lifetime, lifetime)
            data[index] = (DEFAULT_LIFETIME, DEFAULT_LIFETIME)

        for lifetime in fishes_born_today:
            data.append((DEFAULT_LIFETIME + 2, DEFAULT_LIFETIME))
    
    return len(data)