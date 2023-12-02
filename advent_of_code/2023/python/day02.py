from dataclasses import dataclass


@dataclass
class CubeSet:
    red: int = 0
    blue: int = 0
    green: int = 0


def parse() -> list[list[CubeSet]]:
    with open("../input/02.txt", "r") as file:
        l = [s.strip() for s in file.read().strip().split('\n')]
    games = []
    for s in l:
        draws = []
        for set_str in s.partition(":")[2].strip().split(";"):
            set_str = set_str.strip()
            cubeset = CubeSet()
            for pair in set_str.split(", "):
                num, colour = pair.split(" ")
                num = int(num)
                setattr(cubeset, colour, num)
            draws.append(cubeset)
        games.append(draws)
    return games


def q1(games: list[list[CubeSet]]) -> int:
    acc = 0
    for idx, game in enumerate(games):
        for cubeset in game:
            if cubeset.red > 12 or cubeset.green > 13 or cubeset.blue > 14:
                break
        else:
            acc += (idx + 1)  # one-based index
    return acc


def calc_power(game: list[CubeSet]) -> int:
    red = 0
    blue = 0
    green = 0
    for cubeset in game:
        red = max(red, cubeset.red)
        blue = max(blue, cubeset.blue)
        green = max(green, cubeset.green)
    return red * blue * green


def q2(games: list[list[CubeSet]]) -> int:
    return sum(map(calc_power, games))


if __name__ == "__main__":
    games = parse()
    print(q1(games))
    print(q2(games))
