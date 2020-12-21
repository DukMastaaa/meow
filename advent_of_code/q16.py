import re
from functools import reduce

FIELD_PATTERN = re.compile(r"^(.+): (\d+)-(\d+) or (\d+)-(\d+)$")


def parse():
    fields = {}
    my_ticket = []
    nearby_tickets = []
    newline_count = 0
    with open("input/q16.txt", "r") as file:
        for line in file:
            line = line.rstrip()
            if line:
                if newline_count == 0:
                    name, range_1_start, range_1_end, range_2_start, range_2_end = \
                        FIELD_PATTERN.match(line).groups()
                    fields[name] = [
                        (int(range_1_start), int(range_1_end)),
                        (int(range_2_start), int(range_2_end))
                    ]
                elif newline_count == 1 and line[0].isdigit():
                    my_ticket = [int(num) for num in line.split(",")]
                elif newline_count == 2 and line[0].isdigit():
                    nearby_tickets.append([int(num) for num in line.split(",")])
                elif newline_count >= 3:
                    break
            else:
                newline_count += 1
    return fields, my_ticket, nearby_tickets


def get_valid_values(fields):
    valid_values = set()
    for ranges in fields.values():
        for start, end in ranges:
            valid_values.update(set(range(start, end + 1)))
    return valid_values


def part_a():
    fields, _, nearby_tickets = parse()
    valid_values = get_valid_values(fields)

    invalid_values = []
    for ticket in nearby_tickets:
        for value in ticket:
            if value not in valid_values:
                invalid_values.append(value)

    return sum(invalid_values)


def part_b():
    fields, my_ticket, nearby_tickets = parse()
    valid_values = get_valid_values(fields)

    # filter out bad tickets
    invalid_ticket_indexes = []
    for index, ticket in enumerate(nearby_tickets):
        for value in ticket:
            if value not in valid_values:
                invalid_ticket_indexes.append(index)
                break
    invalid_ticket_indexes.reverse()
    for index in invalid_ticket_indexes:
        nearby_tickets.pop(index)

    field_count = len(my_ticket)
    field_names = list(fields.keys())
    possible_fields = [field_names.copy() for _ in range(field_count)]
    names_to_remove = []
    all_tickets = nearby_tickets + [my_ticket]

    # filter out bad fields
    for ticket in all_tickets:
        for index, value in enumerate(ticket):
            if len(possible_fields[index]) == 1:
                continue
            else:
                names_to_remove.clear()
                for field_name in possible_fields[index]:
                    range_1, range_2 = fields[field_name]
                    if not(range_1[0] <= value <= range_1[1]
                           or range_2[0] <= value <= range_2[1]):
                        names_to_remove.append(field_name)
                for field_name in names_to_remove:
                    possible_fields[index].remove(field_name)

    # simplify possible_fields. surely we can improve this
    determined_fields = None
    final_field_order = ["" for _ in range(field_count)]
    while determined_fields or determined_fields is None:
        determined_fields = []
        # simplify lists of length 1
        for index, possible in enumerate(possible_fields):
            if len(possible) == 1:
                determined_fields.append(possible[0])
                final_field_order[index] = possible[0]
        # remove known fields from other possibilities
        for possible in possible_fields:
            for determined_field in determined_fields:
                if determined_field in possible:
                    possible.remove(determined_field)


    return reduce(
        lambda x, y: x * y,
        (value for index, value in enumerate(my_ticket)
         if final_field_order[index].startswith("departure"))
    )


if __name__ == '__main__':
    print(part_a())
    print(part_b())
