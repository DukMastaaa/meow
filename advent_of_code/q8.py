SWITCHER = {"jmp": "nop", "nop": "jmp"}  # i mean it works


def parser():
    instructions = []
    with open("input/q8.txt", "r") as file:
        for line in file:
            line = line.rstrip()
            if line:
                operation, argument = line.split(" ")
                argument = int(argument)
                instructions.append((operation, argument))
    return instructions


def interpreter(instructions):
    accumulator = 0
    instruction_ptr = 0
    visited_addresses = []
    while True:
        if instruction_ptr in visited_addresses:
            exit_reason = "loop"
            break
        elif instruction_ptr >= len(instructions):
            exit_reason = "normal"
            break
        elif instruction_ptr < 0:
            exit_reason = "this should not happen"
            break
        else:
            visited_addresses.append(instruction_ptr)

        operation, argument = instructions[instruction_ptr]
        if operation == "nop":
            instruction_ptr += 1
        elif operation == "acc":
            accumulator += argument
            instruction_ptr += 1
        elif operation == "jmp":
            instruction_ptr += argument
        else:
            raise ValueError("bad operation")
    return exit_reason, accumulator


def part_a():
    instructions = parser()
    exit_reason, accumulator = interpreter(instructions)
    assert exit_reason == "loop"
    return accumulator


def part_b():
    instructions = parser()
    for index, instruction in enumerate(instructions):
        operation, argument = instruction
        if operation in SWITCHER:
            instructions[index] = (SWITCHER[operation], argument)  # swap out the instruction
            exit_reason, accumulator = interpreter(instructions)
            if exit_reason == "normal":
                return accumulator
            instructions[index] = (operation, argument)  # reset the instruction


if __name__ == '__main__':
    print(part_a())
    print(part_b())
