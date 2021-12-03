def get_input():
    with open("../input/03.txt", "r") as file:
        data = [[int(char) for char in line.strip()] for line in file]
    return data


def bool_to_char(b: bool) -> str:
    return "1" if b else "0"


def count_within_cols(row_view):
    return (sum(col) for col in zip(*row_view))


def count_within_one_col(row_view, col: int):
    # todo: aeugh
    return list(count_within_cols(row_view))[col]


def binary_list_to_decimal(binary_list: list[int]) -> int:
    return int("0b" + "".join(str(n) for n in binary_list), 2)


def q1(data):
    counts = list(count_within_cols(data))
    column_length = len(data)

    gamma = binary_list_to_decimal(
        map(lambda n: bool_to_char(n / column_length >= 0.5), counts)
    )
    
    epsilon = binary_list_to_decimal(
        map(lambda n: bool_to_char(n / column_length < 0.5), counts)
    )

    return gamma * epsilon


def q2step(row_view, col: int, column_length: int, do_co2: bool):
    # returns (new_row_view, new_col, new_column_length, do_co2)
    count = count_within_one_col(row_view, col)
    ratio = count / column_length
    
    condition = ratio < 0.5 if do_co2 else ratio >= 0.5

    if condition:
        return list(row for row in row_view if row[col] == 1), col + 1, count, do_co2
    else:
        return list(row for row in row_view if row[col] == 0), col + 1, column_length - count, do_co2


def q2helper(row_view, col, column_length, do_co2):
    assert column_length >= 1

    if column_length == 1 or col >= column_length:
        return list(row_view)[0]

    return q2helper(*q2step(row_view, col, column_length, do_co2))


def q2(data):
    o2_last_item = q2helper(data, 0, len(data), False)
    co2_last_item = q2helper(data, 0, len(data), True)

    o2_rating = binary_list_to_decimal(o2_last_item)
    co2_rating = binary_list_to_decimal(co2_last_item)
    return o2_rating * co2_rating
    

if __name__ == "__main__":
    data = get_input()
    print(q1(data))
    print(q2(data))


# old code


def q1_old(data):
    counters = [0 for _ in range(len(data[0]))]
    for bin_string in data:
        for index, char in enumerate(bin_string):
            counters[index] += 1 if char == "1" else -1
    gamma = "0b" + "".join(map(lambda x: bool_to_char(x >= 0), counters))
    epsilon = "0b" + "".join(map(lambda x: bool_to_char(x < 0), counters))
    return int(gamma, 2) * int(epsilon, 2)