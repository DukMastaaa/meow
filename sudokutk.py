import tkinter as tk
from tkinter import messagebox
from math import floor
from typing import List, Optional, Tuple

Pixel = Tuple[int, int]
Position = Tuple[int, int]
OptPosition = Tuple[Optional[int], Optional[int]]

# some sample sudoku num found on wikipedia
SAMPLE_NUMBER_STR = \
    "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
SAMPLE_NUMBER_STR2 = \
    "435269781682571493197834562826195347374682915951743628519326874248957006763418259"
SAMPLE_NUMBER_STR3 = \
    "435269781682571493197834562826195347374682915951743628519326004248957006763418259"

SAMPLE_NUMBER_STR4 = \
    "435269781000071493197834562826005347374600005951743608510000004248957006763000000"

SAMPLE_NUMBER_STR5 = \
    "400000000000009000000000785007048050001300000006070000860000903700005062003700000"

class BaseGrid(object):
    def __init__(self, number_str: str):
        """
        :param number_str: string with numbers in row-major order.
                           blanks should be 0.
        """
        self.guesses, self.given_locations, self.no_given_locations = \
            self._create_guess(number_str)
        self.notes = self._create_notes()

    @staticmethod
    def _create_guess(number_str: str) -> Tuple[List[List[int]], List[Position], List[Position]]:
        """:returns: (guesses, given_locations, no_given_locations)"""
        guess_list = [[] for _ in range(9)]
        given_locations = []
        no_given_locations = []

        for index, row in enumerate(guess_list):
            row.extend((int(num) for num in number_str[index * 9:(index + 1) * 9]))
        for i in range(9):
            for j in range(9):
                if guess_list[i][j] != 0:
                    given_locations.append((i, j))
                else:
                    no_given_locations.append((i, j))

        return guess_list, given_locations, no_given_locations

    @staticmethod
    def _create_notes() -> List[List[List]]:
        return [[[] for j in range(9)] for i in range(9)]

    @staticmethod
    def _3x3square_bounds(row, col) -> Tuple[int, int, int, int]:
        """
        Returns beginning and end indices for row, col in the current 3x3 square
        selected.
        :returns: Tuple with elements (row_start, row_end, col_start, col_end)
        """
        row_start = 3 * (row // 3)
        row_end = row_start + 3
        col_start = 3 * (col // 3)
        col_end = col_start + 3
        return row_start, row_end, col_start, col_end

    def guess_at(self, row, col) -> int:
        return self.guesses[row][col]

    def notes_at(self, row, col) -> List[int]:
        return self.notes[row][col]

    def is_number_duplicate(self, row, col, num) -> bool:
        """:returns: Whether the same number exists in the same row, col or 3x3 square."""
        for index in range(9):
            if self.guess_at(index, col) == num or self.guess_at(row, index) == num:
                return True
        row_start, row_end, col_start, col_end = self._3x3square_bounds(row, col)
        for i in range(row_start, row_end):
            for j in range(col_start, col_end):
                if self.guess_at(i, j) == num:
                    return True
        return False

    def sudoku_complete(self) -> bool:
        for index in range(9):
            # row, column
            row = self.guesses[index]
            column = list(self.guesses[col_index][index] for col_index in range(9))
            if 0 in row or len(set(row)) != 9 or 0 in column or len(set(column)) != 9:
                return False

            # 3x3 square
            row_start = 3 * (index // 3)
            row_end = 3 * (index // 3 + 1)
            col_start = 3 * (index % 3)
            col_end = 3 * (index % 3 + 1)
            square = (self.guesses[row_index][col_index]
                      for row_index in range(row_start, row_end)
                      for col_index in range(col_start, col_end))
            if len(set(square)) != 9:
                return False
        return True


class GridSolver(BaseGrid):
    def __init__(self, number_str: str):
        super().__init__(number_str)
        self.backtrack = []  # explain this somehow
        self._next_cell_flag = False  # flag

    def calculate_possibilities(self) -> None:
        """Calculates possibilities for each non-given cell and saves in self.notes.

        This does not take other cells' possible values into consideration - possible
        optimisation here, but it would be tough.
        """
        for cell_row, cell_col in self.no_given_locations:
            choices = set(i for i in range(1, 10))
            # rows, cols
            for index in range(9):
                number_on_col = self.guess_at(cell_row, index)
                number_on_row = self.guess_at(index, cell_col)
                if number_on_col in choices:
                    choices.remove(number_on_col)
                if number_on_row in choices:
                    choices.remove(number_on_row)
            # 3x3 square
            row_start, row_end, col_start, col_end = self._3x3square_bounds(cell_row, cell_col)
            for i in range(row_start, row_end):
                for j in range(col_start, col_end):
                    number_in_square = self.guess_at(i, j)
                    if number_in_square in choices:
                        choices.remove(number_in_square)
            self.notes[cell_row][cell_col] = list(choices)

    def guess_simple_possibilities(self) -> None:
        """Guesses cells that only have 1 possible value, and calculates possibilities
        again until it can't be simplified further.
        """
        while True:
            simplified_success = False
            for i, p_row in enumerate(self.notes):
                for j, p_col in enumerate(p_row):
                    if len(p_col) == 1:
                        self.guesses[i][j] = p_col[0]
                        self.no_given_locations.remove((i, j))
                        simplified_success = True
            self.notes = self._create_notes()
            self.calculate_possibilities()
            if not simplified_success:
                break
            # todo: refactor so while has conditional

    def _solve_algorithm(self) -> None:
        """oh boy"""
        self.backtrack = []
        faulty_index = 0  # how on earth do i explain this
        # while len(self.backtrack) != len(self.no_given_locations):
        for beans2 in range(10):
            with open('beans.txt', 'w') as file:
                for beans in range(100000):
                    this_cell_row, this_cell_col = self.no_given_locations[len(self.backtrack)]
                    if self._next_cell_flag or len(self.backtrack) == 0:
                        self._next_cell_flag = False
                        next_possible_idx = 0
                    else:
                        next_possible_idx = faulty_index + 1
                    while True:
                        if next_possible_idx >= len(self.notes_at(this_cell_row, this_cell_col)):
                            # possibilities exhausted for this cell, backtrack
                            if len(self.backtrack) == 0:
                                raise ValueError("Unsolvable")
                            prev_cell_row, prev_cell_col = \
                                self.no_given_locations[len(self.backtrack) - 1]
                            self.guesses[prev_cell_row][prev_cell_col] = 0
                            faulty_index = self.backtrack[-1]
                            self.backtrack.pop()
                            break
                        else:
                            next_possible_guess = \
                                self.notes_at(this_cell_row, this_cell_col)[next_possible_idx]
                            if self.is_number_duplicate(this_cell_row, this_cell_col, next_possible_guess):
                                next_possible_idx += 1
                            else:
                                self.guesses[this_cell_row][this_cell_col] = next_possible_guess
                                self.backtrack.append(next_possible_idx)
                                self._next_cell_flag = True
                                break
                    file.write(str(self.backtrack))
                    file.write("\n")

    def solve(self) -> None:
        self.calculate_possibilities()
        self.guess_simple_possibilities()
        self._solve_algorithm()


class GridModel(BaseGrid):
    def __init__(self, number_str: str):
        super().__init__(number_str)

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
        if self.guess_at(row, col) == 0:
            if num not in self.notes_at(row, col):
                self._add_one_note(row, col, num)
            else:
                self._remove_one_note(row, col, num)

    def _remove_notes_for_guess(self, row, col, num) -> None:
        """Removes notes of same num in 3x3square, row, col of the guess."""
        # traverse same row, same col
        for index in range(9):
            if index != col and num in self.notes_at(row, index):
                self.notes[row][index].remove(num)
            if index != row and num in self.notes_at(index, col):
                self.notes[index][col].remove(num)
        # search through same square
        row_start, row_end, col_start, col_end = self._3x3square_bounds(row, col)
        for i in range(row_start, row_end):
            for j in range(col_start, col_end):
                if i != row and j != col and num in self.notes_at(i, j):
                    self.notes[i][j].remove(num)

    def _add_guess(self, row, col, num) -> None:
        self.guesses[row][col] = num

    def toggle_guess(self, row, col, num) -> None:
        if (row, col) not in self.given_locations:
            if self.guess_at(row, col) == num:
                self._remove_guess(row, col)
            else:
                if self.notes_at(row, col):
                    self.notes[row][col].clear()
                self._add_guess(row, col, num)
                self._remove_notes_for_guess(row, col, num)


class GridView(tk.Canvas):
    def __init__(self, master: tk.Tk, grid_size: int, board_width: int = 600, *args, **kwargs):
        super().__init__(master, bg="white", width=board_width, height=board_width, *args, **kwargs)
        self._master = master
        self._grid_size = grid_size
        self._board_width = board_width
        self._cell_length = board_width // grid_size

        self._BORDER_WIDTH = 1
        self._DIVIDER_THICKNESS = 4
        self._DIVIDER_POS = (
            ((0, 3), (8, 3)), ((0, 6), (8, 6)),
            ((3, 0), (3, 8)), ((6, 0), (6, 8))
        )

        self._selected_row = None
        self._selected_col = None

    def set_selected_cell(self, pos: OptPosition) -> None:
        self._selected_row, self._selected_col = pos

    def get_selected_cell(self) -> OptPosition:
        return self._selected_row, self._selected_col

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

        self.create_rectangle(
            top_left_x, top_left_y, bottom_right_x, bottom_right_y,
            fill="white" if position == self.get_selected_cell() else "light grey",
            outline="orange" if position == self.get_selected_cell() else "black",
            width=self._BORDER_WIDTH
        )

    def _draw_guess(self, position: Position, number: int) -> None:
        text_x, text_y = self._get_centre_coordinate(position)
        self.create_text(text_x, text_y, anchor=tk.CENTER, font="Arial", text=str(number))

    def _draw_given(self, position: Position, number: int) -> None:
        text_x, text_y = self._get_centre_coordinate(position)
        self.create_text(
            text_x, text_y, anchor=tk.CENTER, fill="blue", font="Arial", text=str(number)
        )

    def _draw_notes(self, position: Position, notes: List[int]) -> None:
        # todo: font size?
        note_text = "".join(str(num) for num in notes)
        text_x, text_y = self._get_centre_coordinate(position)
        self.create_text(text_x, text_y, anchor=tk.CENTER, font=("Arial", 10), text=note_text)

    def _draw_dividers(self) -> None:
        half_border_width = self._BORDER_WIDTH // 2

        for index, pair in enumerate(self._DIVIDER_POS):
            top_left_pos, bottom_right_pos = pair
            top_left_corner = "UP-LEFT"
            bottom_right_corner = "DOWN-LEFT" if index < 2 else "UP-RIGHT"

            top_left_x, top_left_y = self._get_corner_coordinate(top_left_pos, top_left_corner)
            bottom_right_x, bottom_right_y = self._get_corner_coordinate(bottom_right_pos,
                                                                         bottom_right_corner)
            if index < 2:
                top_left_x -= half_border_width
                bottom_right_x += half_border_width
            else:
                top_left_y -= half_border_width
                bottom_right_y += half_border_width

            self.create_rectangle(
                top_left_x, top_left_y, bottom_right_x, bottom_right_y,
                fill="black", width=self._BORDER_WIDTH
            )

    def draw_grid(self, guesses: List[List[int]], notes: List[List[List[int]]],
                  given_locations: List[Position]) -> None:
        self.delete(tk.ALL)  # ineffiicenttnttt aaaaaaaaaaaaaaaaaaaaaaaaa
        for row in range(self._grid_size):
            for col in range(self._grid_size):
                self._draw_one_cell((row, col))
                this_guess = guesses[row][col]
                if this_guess != 0:
                    if (row, col) in given_locations:
                        self._draw_given((row, col), this_guess)
                    else:
                        self._draw_guess((row, col), this_guess)
                else:  # just in case there's notes *and* guess for the same cell
                    this_notes = notes[row][col]
                    if this_notes:
                        self._draw_notes((row, col), this_notes)
        self._draw_dividers()


class ToggleButton(tk.Button):
    """Represents a toggle button which changes colour depending on its state."""

    def __init__(self, parent, state_var: tk.BooleanVar, **kwargs):
        super().__init__(parent, **kwargs)
        self._state_var = state_var
        self._state_var.trace_add("write", lambda a, b, c: self._update_appearance())
        self.config(command=self._reverse_state)

    def _update_appearance(self) -> None:
        """(None) Updates the button's appearance."""
        current_state = self._state_var.get()
        self.config(bg="light grey" if current_state else "SystemButtonFace")

    def _reverse_state(self) -> None:
        """(None) Reverses the toggle state."""
        current_state = self._state_var.get()
        self._state_var.set(not current_state)
        # todo: i shouldn't need to be calling this but the trace isn't working for some reason
        self._update_appearance()


class StopwatchFrame(tk.Frame):
    """Represents the section of the status bar which displays the time elapsed."""
    def __init__(self, parent, starting_time: int = 0) -> None:
        self._parent = parent
        super().__init__(self._parent)

        self._current_time = starting_time
        self._is_timing = False

        self._time_display_label = tk.Label(self, text=self.format_time(starting_time),
                                            font=("Arial", 18))
        self._time_display_label.pack(side=tk.TOP, expand=True)

        self._after_ids = []

    @staticmethod
    def format_time(seconds: int) -> str:
        """Returns a string converting the amount of seconds into minutes and seconds.

        Parameters:
            seconds (int): The amount of seconds.

        Returns:
            (str): A string showing the amount of minutes and seconds.
        """
        return f"{seconds // 60}m {seconds % 60:02d}s"

    def set_time(self, seconds: int) -> None:
        """Sets the current time recorded.

        Parameters:
            seconds (int): The time to be set in seconds.

        Returns:
            (None)
        """
        # Multiple after_ids need to be tracked to avoid weird timer behaviour
        # in the first few seconds when spamming the New or Restart Game buttons.
        for after_id in self._after_ids:
            self.after_cancel(after_id)
            self._after_ids.remove(after_id)
        self._current_time = seconds
        self._update_labels()
        new_after_id = self.after(1000, self._update_time)
        self._after_ids.append(new_after_id)

    def start_timing(self) -> None:
        """(None) Starts recording the time."""
        if not self._is_timing:
            self._is_timing = True
            self.after(1000, self._update_time)

    def stop_timing(self) -> None:
        """(None) Stops recording the time."""
        self._is_timing = False

    def get_time(self) -> int:
        """(int) Returns the recorded time in seconds."""
        return self._current_time

    def _update_time(self) -> None:
        """(None) Increments the current time every second as long as self._is_timing == True."""
        for after_id in self._after_ids:
            self.after_cancel(after_id)
            self._after_ids.remove(after_id)
        if self._is_timing:
            self._current_time += 1
            self._update_labels()
            new_after_id = self.after(1000, self._update_time)
            self._after_ids.append(new_after_id)

    def _update_labels(self) -> None:
        """(None) Update the time reading on the labels."""
        self._time_display_label.config(text=self.format_time(self._current_time))


# todo: timer, difficulty setting, help


class SudokuController(object):
    def __init__(self, master: tk.Tk, number_str: str) -> None:
        self._master = master

        self._timer = StopwatchFrame(self._master, 0)
        self._timer.pack(side=tk.TOP)

        self._note_mode = tk.BooleanVar()
        self._note_mode.set(False)
        self._grid = GridModel(number_str)
        self._view = GridView(self._master, 9, 600)

        self._view.bind("<Button-1>", self.left_click)
        bind_helper = lambda num: (lambda e: self.number_press(num))
        for i in range(1, 10):
            self._master.bind(str(i), bind_helper(i))
        self._master.bind("<BackSpace>", lambda e: self.backspace())
        self._master.bind("<Escape>", lambda e: self.escape())
        self._master.bind("n", lambda e: self.toggle_note_mode())

        self._view.pack(side=tk.TOP, anchor=tk.N)
        self.redraw()

        self._note_button = ToggleButton(self._master, self._note_mode, text="note mode")
        self._note_button.pack(side=tk.TOP)

        self._timer.start_timing()

    def redraw(self) -> None:
        self._view.draw_grid(self._grid.guesses, self._grid.notes, self._grid.given_locations)

    def left_click(self, event) -> None:
        try:
            clicked_cell = self._view.pixel_to_position((event.x, event.y))
        except ValueError:
            return None
        if clicked_cell != self._view.get_selected_cell():
            self._view.set_selected_cell(clicked_cell)
        else:
            self._view.set_selected_cell((None, None))
        self.redraw()

    def backspace(self) -> None:
        self._grid.clear_cell(*self._view.get_selected_cell())
        self.redraw()

    def escape(self) -> None:
        self._view.set_selected_cell((None, None))
        self.redraw()

    def toggle_note_mode(self) -> None:
        self._note_mode.set(not self._note_mode.get())

    def number_press(self, number: int) -> None:
        cell = self._view.get_selected_cell()
        if cell != (None, None):
            if self._note_mode.get():
                self._grid.toggle_note(*self._view.get_selected_cell(), number)
            else:
                self._grid.toggle_guess(*self._view.get_selected_cell(), number)
            self.redraw()
            self.check_valid()

    def check_valid(self) -> None:
        if self._grid.sudoku_complete():
            self.stop_game()

    def stop_game(self) -> None:
        self._timer.stop_timing()
        finish_time = self._timer.format_time(self._timer.get_time())
        messagebox.showinfo(title=f"nice", message=f"gj, you took {finish_time}!")


class SudokuApp(object):  # need on_window_close() to stop timer
    def __init__(self, master: tk.Tk) -> None:
        self._master = master
        self.controller = SudokuController(self._master, SAMPLE_NUMBER_STR)


def main():
    global app
    root = tk.Tk()
    app = SudokuApp(root)
    # root.protocol("WM_DELETE_WINDOW", app.on_window_close)
    root.mainloop()

def test():
    g = GridSolver(SAMPLE_NUMBER_STR5)
    g.solve()
    print(g.guesses)


if __name__ == '__main__':
    # main()
    test()
