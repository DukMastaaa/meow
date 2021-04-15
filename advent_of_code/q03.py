# oop time
from functools import reduce
from typing import List
EMPTY = "."
TREE = "#"


class Board(object):
    def __init__(self, charlist: List[List[str]]):
        self.charlist = charlist
        self.width = len(self.charlist[0])
        self.height = len(self.charlist)

    def at(self, row, col):
        return self.charlist[row][col]


class Cursor(object):
    def __init__(self, board: Board):
        self.board = board
        self.x = 0
        self.y = 0

    def reset_pos(self):
        self.x = 0
        self.y = 0

    def move_x(self, num: int, reverse: bool = False):
        for _ in range(num):
            if not reverse:
                if self.x + 1 >= self.board.width:
                    self.x = 0
                else:
                    self.x += 1
            else:
                if self.x - 1 <= 0:
                    self.x = self.board.width - 1
                else:
                    self.x -= 1

    def move_y(self, num: int, reverse: bool = False):
        if not reverse:
            self.y += num
        else:
            self.y -= num

    def at(self):
        return self.board.at(self.y, self.x)


def setup():
    filelist = []
    with open('input/q3.txt', 'r') as file:
        for line in file:
            filelist.append(list(line.strip()))
    board = Board(filelist)
    cursor = Cursor(board)
    return board, cursor


def calculate(slopes):
    board, cursor = setup()
    tree_list = []

    for slope_x, slope_y in slopes:
        trees = 0
        cursor.reset_pos()
        while cursor.y < board.height:
            if cursor.at() == TREE:
                trees += 1
            cursor.move_x(slope_x)
            cursor.move_y(slope_y)
        tree_list.append(trees)
    return reduce((lambda x, y: x * y), tree_list)


def part_a():
    return calculate([(3, 1)])


def part_b():
    return calculate([(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)])


if __name__ == '__main__':
    print(part_a())
