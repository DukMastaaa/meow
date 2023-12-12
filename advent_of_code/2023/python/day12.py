from functools import lru_cache
from itertools import repeat


def parse() -> list[tuple[str, list[int]]]:
    data = []
    with open("../input/12.txt", "r") as file:
        for line in file.read().strip().split("\n"):
            record, right = line.split(" ")
            counts = list(map(int, right.split(",")))
            data.append((record, counts))
    return data


def calculate_pattern(counts: list[int]) -> str:
    """
    Returns a pattern (like a regex) which all valid arrangements must match.
    `.` and `#` have their original meanings, and `*` means any number of `.` characters.
    """
    return "*" + ".*".join("#" * count for count in counts) + "*"


def solve(record: str, pattern: str) -> int:
    len_record = len(record)
    len_pattern = len(pattern)
    
    @lru_cache()
    def helper(r: int, p: int) -> int:
        """r and p are indexes into record and pattern."""
        
        # if pattern exhausted and we haven't reached end of record
        if p >= len_pattern and r <= len_record - 1:
            return 0  # fail
        # if end of record but pattern not exhausted
        if r >= len_record:
            if p <= len_pattern - 2:  # -2 since * at end of pattern
                return 0  # fail
            else:
                return 1  # success
        
        rc = record[r]
        tc = pattern[p]
        if rc == "?":
            if tc == "*":
                return (  # fork possibilities.
                    # 1. add a period.
                    helper(r + 1, p)
                    +
                    # 2. skip to the next pattern char.
                    helper(r, p + 1)
                )
            else:
                # must add whatever the pattern prescribes.
                return helper(r + 1, p + 1)
        elif tc == "*":
            if rc == "#":
                # no zeros here. continue on the pattern.
                return helper(r, p + 1)
            else:
                # rc == "." matches with the pattern.
                return helper(r + 1, p)
        else:
            # ensure pattern agrees with the record
            return helper(r + 1, p + 1) if rc == tc else 0
    
    helper.cache_clear()
    return helper(0, 0)


def q1_to_q2_data(q1_data: list[tuple[str, list[int]]]) -> list[tuple[str, list[int]]]:
    return [
        ("?".join(repeat(record, 5)), counts * 5)
        for record, counts in q1_data
    ]


def general_solution(data: list[tuple[str, list[int]]]) -> int:
    return sum(
        solve(record, calculate_pattern(counts))
        for record, counts in data
    )


if __name__ == "__main__":
    q1_data = parse()
    q2_data = q1_to_q2_data(q1_data)
    print(general_solution(q1_data))
    print(general_solution(q2_data))
