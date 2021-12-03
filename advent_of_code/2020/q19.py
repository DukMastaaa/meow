def parse():
    rules = {}
    messages = []
    messages_flag = False
    with open("input/q19test.txt", "r") as file:
        for line in file:
            line = line.rstrip()
            if not line:
                if not messages_flag:
                    messages_flag = True
                    continue
                else:
                    break
            if messages_flag:
                messages.append(line)
            else:
                rule_num, _, temp_matches = line.partition(":")
                rule_num = int(rule_num)
                if "a" in temp_matches:
                    rules[rule_num] = "a"
                elif "b" in temp_matches:
                    rules[rule_num] = "b"
                else:
                    temp_matches = temp_matches.strip().split("|")
                    matches = (rule_set.strip().split(" ") for rule_set in temp_matches)
                    matches = tuple(tuple(int(num) for num in match) for match in matches)
                    rules[rule_num] = matches
    return rules, messages


def check(rules, message, rule_num, starting_index):
    if starting_index >= len(message):  # message too short to match!
        return -1

    current_rules = rules[rule_num]

    if type(current_rules) == str:
        if message[starting_index] == current_rules:
            return starting_index + 1
        else:
            return -1

    else:
        for rule_list in current_rules:
            new_starting_index = starting_index
            for rule in rule_list:
                output = check(rules, message, rule, new_starting_index)
                if output == -1:  # this branch is bad
                    new_starting_index = starting_index
                    break
                else:
                    new_starting_index = output
            else:  # this triggers if no break
                # need to check for trailing chars - if they exist, no match
                if rule_num == 0:
                    if new_starting_index != len(message):
                        continue
                return new_starting_index
        else:
            return -1


def part_a():
    rules, messages = parse()
    match_counter = 0
    for message in messages:
        status = check(rules, message, 0, 0)
        if status == len(message):
            match_counter += 1
    return match_counter


def part_b():
    rules, messages = parse()
    rules[8] = ((42,), (42, 8))
    rules[11] = ((42, 31), (42, 11, 31))
    match_counter = 0
    for message in messages:
        status = check(rules, message, 0, 0)
        if status != -1:
            match_counter += 1
    return match_counter


if __name__ == '__main__':
    # print(part_a())
    # print(part_b())
    r, _ = parse()
    print(check(r, "baa", 0, 0))
