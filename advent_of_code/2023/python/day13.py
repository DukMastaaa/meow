import numpy as np


def parse() -> list[list[str]]:
    patterns = []
    t = []
    with open("../input/13.txt", "r") as file:
        for line in file.read().strip().split("\n"):
            if line != "":
                t.append(line)
            else:
                patterns.append(t)
                t = []
        patterns.append(t)
    return patterns


def check_pattern_rows(pattern: list[str]) -> int:
    height = len(pattern)
    duplicate_idxs = [
        bottom_idx for bottom_idx in range(1, height)
        if pattern[bottom_idx-1] == pattern[bottom_idx]
    ]
    for i in duplicate_idxs:
        # attempt to follow the reflection
        rows_after = height - (i + 1)
        rows_before = i - 1
        for j in range(min(rows_after, rows_before)):
            idx_after = i + 1 + j
            idx_before = i - 2 - j
            if pattern[idx_before] != pattern[idx_after]:
                break
        else:
            # reflection found
            return i
    return 0


def transpose_pattern(pattern: list[str]) -> list[str]:
    return list(map(lambda ts: "".join(ts), zip(*pattern)))


def get_correct_rowcol(patterns: list[list[str]]) -> list[tuple[int, int]]:
    return [
        (check_pattern_rows(transpose_pattern(p)), check_pattern_rows(p))
        for p in patterns
    ]


def summary(rowcol: list[tuple[int, int]]) -> int:
    return sum(right_idx + 100 * bottom_idx for right_idx, bottom_idx in rowcol)


def swap(rowcol: tuple[int, int]) -> tuple[int, int]:
    return rowcol[1], rowcol[0]


def find_smudge_rows(pattern: list[str], correct_row: int) -> tuple[int, int]:
    # too tired to clean this up and unify with part 1
    def helper(pattern: list[str], correct_row: int) -> tuple[int, int]:
        height = len(pattern)
        duplicate_idxs = []
        for i in range(1, height):
            if i == correct_row:
                continue
            wrong_counts = sum(int(c1 != c2) for c1, c2 in zip(pattern[i-1], pattern[i]))
            if wrong_counts == 1:
                duplicate_idxs.append((i, True))
            elif wrong_counts == 0:
                duplicate_idxs.append((i, False))

        for i, used_already in duplicate_idxs:
            # attempt to follow the reflection
            rows_after = height - (i + 1)
            rows_before = i - 1
            for j in range(min(rows_after, rows_before)):
                idx_after = i + 1 + j
                idx_before = i - 2 - j
                wrong_counts = sum(int(c1 != c2) for c1, c2 in zip(pattern[idx_before], pattern[idx_after]))
                if not used_already and wrong_counts == 1:
                    used_already = True
                # debugging the below line took 80min. i had `elif used_already and wrong_counts != 0`
                elif wrong_counts != 0:
                    break
            else:
                # reflection found
                return (0, i)
        
        return (0, 0)
    
    if (x := helper(pattern, correct_row)) != (0, 0):
        return x
    elif (y := swap(helper(transpose_pattern(pattern), -1))) != (0, 0):
        return y
    else:
        raise ValueError


def get_smudged_rowcol(patterns: list[list[str]],
                       correct_rowcol: list[tuple[int, int]]) -> list[tuple[int, int]]:
    assert (0, 0) not in patterns
    return [
        swap(find_smudge_rows(transpose_pattern(p), right))
        if right != 0
        else find_smudge_rows(p, bottom)
        for (right, bottom), p in zip(correct_rowcol, patterns)
    ]


if __name__ == "__main__":
    patterns = parse()
    correct_rowcol = get_correct_rowcol(patterns)
    q1 = summary(correct_rowcol)
    smudged_rowcol = get_smudged_rowcol(patterns, correct_rowcol)
    q2 = summary(smudged_rowcol)
    print(q1, q2)
