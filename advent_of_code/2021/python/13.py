Position = tuple[int, int]


def get_input():
    paper = set()
    folds = []
    with open("../input/13.txt", "r") as file:
        while line := file.readline().strip():
            x, y = line.split(",")
            paper.add((int(x), int(y)))
        for line in file:
            line = line.lstrip("fold along ")
            direction, coord = line.split("=")
            folds.append((direction, int(coord)))
    return paper, folds


def fold_point(point: Position, direction: str, fold_coord: int) -> Position:
    x, y = point
    if direction == "x":
        if x > fold_coord:
            return (fold_coord - abs(fold_coord - x), y)
    else:
        if y > fold_coord:
            return (x, fold_coord - abs(fold_coord - y))
    return (x, y)


def fold(paper: set[Position], folds: list[tuple[str, int]], iterations: int = None):
    for iteration, (fold_dir, fold_coord) in enumerate(folds):
        if iterations is not None and iteration >= iterations:
            break

        points_to_remove = set()
        points_to_add = set()

        for point in paper:
            image = fold_point(point, fold_dir, fold_coord)
            if image != point:
                points_to_remove.add(point)
                points_to_add.add(image)
        
        paper.difference_update(points_to_remove)
        paper.update(points_to_add)
    
    return paper


def display_paper(paper: set[Position]):
    width = max(pos[0] for pos in paper)
    height = max(pos[1] for pos in paper)
    for x in range(0, width + 1):
        for y in range(0, height + 1):
            if (x, y) in paper:
                print("#", end="")
            else:
                print(".", end="")
        print("")


def q1(paper, folds):
    return len(fold(paper, folds, 1))


def q2(paper, folds):
    fold(paper, folds)
    display_paper(paper)


if __name__ == "__main__":
    q1data = get_input()
    print(q1(*q1data))

    q2data = get_input()
    q2(*q2data)
