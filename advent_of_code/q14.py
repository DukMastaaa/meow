import re
MASK_PATTERN = re.compile(r"^mask = ([01X]+)$")
ADDR_PATTERN = re.compile(r"^mem\[(\d+)\] = (\d+)$")


def mask_to_list(mask: str):
    # todo: comprehension?
    mask_list = []
    for index, char in enumerate(mask[::-1]):
        if char != "X":
            mask_list.append((index, char))
    return mask_list


def int_to_bytes(base_10_number):
    byte_str = bin(base_10_number)[2:]
    return "0" * (36 - len(byte_str)) + byte_str


def bytes_to_int(byte_str):
    return int(byte_str, 2)


def part_a():
    def apply_mask(applied_value, mask_list) -> str:
        new_value = list(applied_value)
        for index, char in mask_list:
            new_value[len(new_value) - 1 - index] = char
        return "".join(new_value)

    memory = {}
    mask_list = []
    with open("input/q14.txt", "r") as file:
        for line in file:
            line = line.rstrip()
            if line:
                if line.startswith("mask"):
                    mask_str = MASK_PATTERN.match(line).group(1)
                    mask_list = mask_to_list(mask_str)
                elif line.startswith("mem"):
                    address, value = ADDR_PATTERN.match(line).groups()
                    address = int(address)
                    value = int_to_bytes(int(value))
                    memory[address] = apply_mask(value, mask_list)
    return sum(bytes_to_int(value) for value in memory.values())


def generate_binary_sequence(bit_count):
    """generates (0, 0, ..., 0), (0, 0, ..., 1), (0, ..., 1, 0), etc."""
    for i in range(2**bit_count):
        binary = bin(i)[2:]
        yield tuple("0" * (bit_count - len(binary)) + binary)


def part_b():
    def apply_mask(address_bytes, mask):
        """returns new addresses to modify"""
        address_list = list(address_bytes)
        floating_bits = []
        addresses_to_overwrite = []
        for index, char in enumerate(mask):
            if char == "0":
                continue
            elif char == "1":
                address_list[index] = "1"
            elif char == "X":
                floating_bits.append(index)

        for bits in generate_binary_sequence(len(floating_bits)):
            for iter_index, floating_index in enumerate(floating_bits):
                address_list[floating_index] = bits[iter_index]
            new_address_as_str = "".join(address_list)
            addresses_to_overwrite.append(bytes_to_int(new_address_as_str))
        return addresses_to_overwrite

    memory = {}
    mask = ""
    with open("input/q14.txt", "r") as file:
        for line in file:
            line = line.rstrip()
            if line.startswith("mask"):
                mask = MASK_PATTERN.match(line).group(1)
            elif line.startswith("mem"):
                address, value = ADDR_PATTERN.match(line).groups()
                address = int_to_bytes(int(address))
                value = int(value)
                addresses_to_modify = apply_mask(address, mask)
                for new_address in addresses_to_modify:
                    memory[new_address] = value
    return sum(value for value in memory.values())


if __name__ == '__main__':
    print(part_a())
    print(part_b())
