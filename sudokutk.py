import tkinter as tk
from math import floor
from typing import List, Optional, Tuple


Pixel = Tuple[int, int]
Position = Tuple[int, int]

# some sample sudoku i found on wikipedia
SAMPLE_NUMBER_STR = \
    "530070000600195000098000060800060003400803001700020006060000280000419005000080079"


class Grid(object):
    def __init__(self, number_str: str):
        """
        :param number_str: string with numbers in row-major order.
                           blanks should be 0.
        """
        self.guesses = self._create_guess(number_str)
        self.notes = self._create_notes()

    @staticmethod
    def _create_guess(number_str: str) -> List[List[int]]:
        guess_list = [[] for _ in range(9)]
        for index, row in enumerate(guess_list):
            row.extend(number_str[index*9:(index+1)*9])
        return guess_list

    @staticmethod
    def _create_notes() -> List[List[List]]:
        return [[[] for j in range(9)] for i in range(9)]

    @staticmethod
    def _current_3x3square_bounds(row, col) -> Tuple[int, int, int, int]:
        """
        Returns beginning and end indices for row, col in the current 3x3 square
        selected.
        :returns: Tuple with elements (row_start, row_end, col_start, col_end)
        """
        row_start = row // 3
        row_end = row_start + 1
        col_start = col // 3
        col_end = col_start + 1
        return row_start, row_end, col_start, col_end

    def guess_at(self, row, col) -> int:
        return self.guesses[row][col]

    def notes_at(self, row, col) -> List[int]:
        return self.notes[row][col]

    def _remove_guess(self, row, col) -> None:
        self.guesses[row][col] = 0

    def _remove_all_notes(self, row, col) -> None:
        self.notes[row][col].clear()

    def clear_cell(self, row, col) -> None:
        self._remove_guess(row, col)
        self._remove_all_notes(row, col)

    def _remove_one_note(self, row, col, num) -> None:
        self.notes[row][col].remove(num)

    def _add_one_note(self, row, col, num) -> None:
        self.notes[row][col].append(num)

    def toggle_note(self, row, col, num) -> None:
        assert num != 0
        if self.guess_at(row, col) != 0:
            if num not in self.notes_at(row, col):
                self._add_one_note(row, col, num)
            else:
                self._remove_one_note(row, col, num)

    def _remove_hints_for_guess(self, row, col, num) -> None:
        """Removes hints of same num in 3x3square, row, col of the guess."""
        # traverse same row, same col
        for index in range(9):
            if index != col and num in self.notes_at(row, index):
                self.notes[row][index].remove(num)
            if index != row and num in self.notes_at(index, col):
                self.notes[index][col].remove(num)
        # search through same square
        row_start, row_end, col_start, col_end = self._current_3x3square_bounds(row, col)
        for i in range(row_start, row_end):
            for j in range(col_start, col_end):
                if i != row and j != col and num in self.notes_at(i, j):
                    self.notes[i][j].remove(num)

    def _add_guess(self, row, col, num) -> None:
        self.guesses[row][col] = num

    def toggle_guess(self, row, col, num) -> None:
        if self.guess_at(row, col) == num:
            self._remove_guess(row, col)
        else:
            if self.notes_at(row, col):
                self.notes[row][col].clear()
            self._add_guess(row, col, num)


class GridView(tk.Canvas):
    def __init__(self, master: tk.Tk, grid_size: int, board_width: int = 600, *args, **kwargs):
        super().__init__(master, bg="white", width=board_width, height=board_width, *args, **kwargs)
        self._master = master
        self._grid_size = grid_size
        self._board_width = board_width
        self._cell_length = board_width // grid_size
        self._BORDER_WIDTH = 1

    def check_valid_position(self, pixel: Pixel) -> None:
        pixel_x, pixel_y = pixel
        if max(pixel_x, pixel_y) >= self._board_width or min(pixel_x, pixel_y) < 0:
            raise ValueError

    def pixel_to_position(self, pixel: Pixel) -> Position:
        self.check_valid_position(pixel)
        pixel_x, pixel_y = pixel
        row = pixel_y // self._cell_length
        column = pixel_x // self._cell_length
        return row, column

    def _get_corner_coordinate(self, cell_position: Position, corner: str) -> Pixel:
        row, column = cell_position

        pixel_x_multiplier = column
        pixel_y_multiplier = row

        if "RIGHT" in corner:
            pixel_x_multiplier += 1
        if "DOWN" in corner:
            pixel_y_multiplier += 1

        border_compensation_x = self._BORDER_WIDTH * (-1 if "RIGHT" in corner else 0)
        border_compensation_y = self._BORDER_WIDTH * (-1 if "DOWN" in corner else 0)

        pixel_x = pixel_x_multiplier * self._cell_length + border_compensation_x
        pixel_y = pixel_y_multiplier * self._cell_length + border_compensation_y
        return pixel_x, pixel_y

    def _get_centre_coordinate(self, position: Position) -> Pixel:
        row, column = position
        pixel_x = floor((column + 0.5) * self._cell_length)
        pixel_y = floor((row + 0.5) * self._cell_length)
        return pixel_x, pixel_y

    def _draw_one_cell(self, position: Position) -> None:
        top_left_x, top_left_y = self._get_corner_coordinate(position, "UP-LEFT")
        bottom_right_x, bottom_right_y = self._get_corner_coordinate(position, "DOWN-RIGHT")

        self.create_rectangle(top_left_x, top_left_y, bottom_right_x, bottom_right_y,
                              fill="grey", outline="black", width=self._BORDER_WIDTH,
                              activeoutline="orange", activewidth=(self._BORDER_WIDTH + 1))

    def _draw_guess(self, position: Position, number: int) -> None:
        text_x, text_y = self._get_centre_coordinate(position)
        self.create_text(text_x, text_y, anchor=tk.CENTER, font="Arial", text=str(number))

    def _draw_notes(self, position: Position, notes: List[int]) -> None:
        # todo: font size?
        note_text = "".join(str(num) for num in notes)
        text_x, text_y = self._get_centre_coordinate(position)
        self.create_text(text_x, text_y, anchor=tk.CENTER, font=("Arial", 8), text=note_text)

    def draw_grid(self, guesses: List[List[int]], notes: List[List[List[int]]]) -> None:
        self.delete(tk.ALL)  # ineffiicenttnttt aaaaaaaaaaaaaaaaaaaaaaaaa
        for row_index in range(self._grid_size):
            for column_index in range(self._grid_size):
                self._draw_one_cell((row_index, column_index))

                this_guess = guesses[row_index][column_index]
                if this_guess != 0:
                    self._draw_guess((row_index, column_index), this_guess)
                else:  # just in case there's notes *and* guess for the same cell
                    this_notes = notes[row_index][column_index]
                    if this_notes:
                        self._draw_notes((row_index, column_index), this_notes)

# class NoteButton(tk.Button):
#     def __init__(self, parent, *args, **kwargs) -> None:
#         super().__init__(parent, *args, **kwargs)
#         self._parent = parent


# todo: timer, note button, difficulty setting


class SudokuController(object):
    def __init__(self, master: tk.Tk, number_str: str) -> None:
        self._master = master

        self._note_mode = tk.BooleanVar()
        self._note_mode.set(False)

        self._grid = Grid(number_str)
        self._view = GridView(self._master, 9, 600)




class SudokuApp(object):  # need on_window_close() to stop timer
    def __init__(self, master: tk.Tk) -> None:
        self._master = master
        self.controller = SudokuController(self._master, SAMPLE_NUMBER_STR)


def main():
    root = tk.Tk()
    app = SudokuApp(root)
    root.protocol("WM_DELEE_WINDOW", app.on_window_close)
    root.mainloop()


if __name__ == '__main__':
    main()
