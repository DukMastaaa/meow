from itertools import product

BOARD_LENGTH = 5
position = tuple[int, int]


class Board:
    # assumes that board_list elements are unique.

    def __init__(self, board_dict: dict[int, position], marks: set[int]):
        self.value_to_position = board_dict
        self.position_to_value = {val: key for key, val in board_dict.items()}
        self.marks = marks
    
    @staticmethod
    def list_to_board_dict(board_list: list[list[int]]) -> dict[int, position]:
        output = {}
        for row_idx, row in enumerate(board_list):
            for col_idx, num in enumerate(row):
                output[num] = (row_idx, col_idx)
        return output

    def draw_number(self, num: int) -> None:
        position = self.value_to_position.get(num)
        if position is not None:
            self.marks.add(position)
    
    def check_win(self) -> bool:
        # todo: any way to eliminate duplication?
        return any(
            all(
                pos in self.marks
                for pos in product([row], range(BOARD_LENGTH))
            )
            for row in range(BOARD_LENGTH)
        ) or any(
            all(
                pos in self.marks
                for pos in product(range(BOARD_LENGTH), [col])
            )
            for col in range(BOARD_LENGTH)
        )
    
    def final_score(self, most_recent_draw: int) -> int:
        undrawn_sum = sum(
            self.position_to_value[pos] 
            for pos in product(range(BOARD_LENGTH), range(BOARD_LENGTH)) 
            if pos not in self.marks
        )
        return undrawn_sum * most_recent_draw


def get_input() -> tuple[list[int], Board]:
    with open("../input/04.txt", "r") as file:
        drawn_numbers = [int(num) for num in file.readline().strip().split(",")]
        file.readline()  # newline

        boards = []
        this_board_list = []
        for line in file:
            line = line.rstrip()
            if line == "":
                this_board_dict = Board.list_to_board_dict(this_board_list)
                boards.append(Board(this_board_dict, set()))
                this_board_list = []
            else:
                this_board_list.append(int(num) for num in line.split(" ") if num != "")

    return drawn_numbers, boards


def combined_solution(data: tuple[list[int], Board], run_q2: bool) -> int:
    drawn_numbers, boards = data
    for draw in drawn_numbers:
        finished_board_indices = []
        
        for index, board in enumerate(boards):
            board.draw_number(draw)
            if board.check_win():
                finished_board_indices.append(index)   
                if not run_q2 or (run_q2 and len(boards) == 1):
                    return board.final_score(draw)

        if run_q2:
            for index in reversed(finished_board_indices):
                boards.pop(index)
    
    return -1


if __name__ == "__main__":
    q1data = get_input()
    q2data = get_input()
    print(combined_solution(q1data, False))  # q1
    print(combined_solution(q1data, True))   # q2


# old code is just separating run_q2 case out of the combined_solution.
