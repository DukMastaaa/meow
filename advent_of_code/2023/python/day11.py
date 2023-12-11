Pos = tuple[int, int]


def parse() -> tuple[list[Pos], set[int], set[int]]:
    with open("../input/11.txt", "r") as file:
        l = [s.strip() for s in file.read().strip().split('\n')]
    points = []
    for i, line in enumerate(l): 
        for j, c in enumerate(line):
            if c == "#":
                points.append((i, j))
    height = len(l)
    width = len(l[0])
    empty_rows = set(range(height)).difference(set(i for i, j in points))
    empty_cols = set(range(width)).difference(set(j for i, j in points))
    return points, empty_rows, empty_cols


def distance(p1: Pos, p2: Pos,
             empty_rows: set[int], empty_cols: set[int],
             gap_length: int) -> int:
    p1y, p1x = p1
    p2y, p2x = p2
    # set(range) is so inefficient but the grid isn't that large so :shrug:
    empty_rows_traversed = len(empty_rows.intersection(set(range(min(p1y, p2y), max(p1y, p2y)))))
    empty_cols_traversed = len(empty_cols.intersection(set(range(min(p1x, p2x), max(p1x, p2x)))))
    return (abs(p2y - p1y) + empty_rows_traversed * (gap_length - 1)) \
        + (abs(p2x - p1x) + empty_cols_traversed * (gap_length - 1))


def general_solution(points: list[Pos],
                     empty_rows: set[int], empty_cols: set[int],
                     gap_length: int) -> int:
    total_points = len(points)
    return sum(
        distance(points[i1], points[i2], empty_rows, empty_cols, gap_length)
        for i1 in range(total_points) for i2 in range(i1 + 1, total_points)
    )


if __name__ == "__main__":
    points, empty_rows, empty_cols = parse()
    print(general_solution(points, empty_rows, empty_cols, 2))
    print(general_solution(points, empty_rows, empty_cols, 1_000_000))
