from functools import reduce
from typing import Tuple, Callable

TIMES = "*"
PLUS = "+"
OPERATION = {
    TIMES: lambda x, y: x * y,
    PLUS: lambda x, y: x + y
}


def calc_a(expression: str) -> int:
    """calculates an expression with + and *. operator precedence
    is equal, evaluated left to right. assumes no parentheses"""
    expression = expression.strip()
    tokens = [int(token) if token.isdigit() else token for token in expression.split(" ")]
    answer = tokens[0]
    operator = ""
    for token in tokens[1:]:
        if token in OPERATION:
            operator = token
        else:
            answer = OPERATION[operator](answer, token)
    return answer


def calc_b(expression: str) -> int:
    """calculates an expression with + and *. addition has higher precedence
    than multiplication, evaluated left to right. assumes no parentheses"""
    expression = expression.strip()
    tokens = [int(token) if token.isdigit() else token for token in expression.split(" ")]
    while PLUS in tokens:
        plus_index = tokens.index(PLUS)
        addition = tokens[plus_index-1] + tokens[plus_index+1]
        del tokens[plus_index-1:plus_index+2]
        tokens.insert(plus_index - 1, addition)
    return reduce(OPERATION[TIMES], (num for num in tokens if type(num) == int))


def innermost_parens(line: str) -> Tuple[int, int]:
    """returns indexes of the innermost set of parentheses starting from the left.
    assumes parentheses are balanced and there are parentheses in the line."""
    close_index = line.index(")")
    for i in range(close_index - 1, -1, -1):
        if line[i] == "(":
            open_index = i
            return open_index, close_index


def eval_one_line(line: str, calculator: Callable) -> int:
    line = line.strip()
    while "(" in line:
        open_index, close_index = innermost_parens(line)
        answer = calculator(line[open_index + 1:close_index])
        line = line[:open_index] + str(answer) + line[close_index+1:]
    return calculator(line)


def driver(calculator: Callable):
    counter = 0
    with open("input/q18.txt", "r") as file:
        for line in file:
            line = line.rstrip()
            if line:
                counter += eval_one_line(line, calculator)
    return counter


def part_a():
    return driver(calc_a)


def part_b():
    return driver(calc_b)


if __name__ == '__main__':
    print(part_a())
    print(part_b())
