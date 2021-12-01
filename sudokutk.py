# ducky's sudoku program in tkinter

import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from math import floor
from typing import List, Optional, Tuple
from random import sample, randint, choice

Pixel = Tuple[int, int]
Position = Tuple[int, int]
OptPosition = Tuple[Optional[int], Optional[int]]


class BaseGrid(object):
    """Base class for all grid objects."""

    def __init__(self):
        self.guesses = None
        self.given_locations = None
        self.no_given_locations = None
        self.notes = None

    def reset(self) -> None:
        """Resets the grid."""
        self.guesses = None
        self.given_locations = None
        self.no_given_locations = None
        self.notes = None

    def get_number_str(self) -> str:
        """Turns self.guesses into a string of numbers in row-major order"""
        return "".join("".join(str(num) for num in line) for line in self.guesses)

    def setup(self, number_str: str) -> None:
        """Creates stuff like self.guesses, self.given_locations etc.

        :param number_str: string with numbers in row-major order.
                           blanks should be 0.
        """
        self.guesses, self.given_locations, self.no_given_locations = \
            self._create_guess(number_str)
        self.notes = self._create_notes()

    @staticmethod
    def _create_guess(number_str: str) -> Tuple[List[List[int]], List[Position], List[Position]]:
        """Returns (guesses, given_locations, no_given_locations)."""
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
        """Creates empty note list."""
        return [[[] for _ in range(9)] for _ in range(9)]

    @staticmethod
    def _3x3square_bounds(row, col) -> Tuple[int, int, int, int]:
        """Returns beginning and end indices for row, col in the current 3x3 square
        selected.

        :returns: Tuple with elements (row_start, row_end, col_start, col_end)
        """
        row_start = 3 * (row // 3)
        row_end = row_start + 3
        col_start = 3 * (col // 3)
        col_end = col_start + 3
        return row_start, row_end, col_start, col_end

    def guess_at(self, row, col) -> int:
        """Returns the guess at the specified cell."""
        return self.guesses[row][col]

    def notes_at(self, row, col) -> List[int]:
        """Returns notes at the specified cell."""
        return self.notes[row][col]

    def is_number_duplicate(self, row, col, num) -> bool:
        """Returns whether the same number exists in the same row, col or 3x3 square."""
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
        """Checks whether the grid is valid and complete."""
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
    """Solves a Sudoku grid using a recursive backtracking algorithm."""

    def __init__(self):
        super().__init__()
        self.backtrack = None
        self._next_cell_flag = None

    def setup(self, number_str: str) -> None:
        """Supplies the unsolved grid to solve."""
        super().setup(number_str)
        self.backtrack = []  # used for backtracking in algorithm
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
        simplified_success = True
        while simplified_success:
            simplified_success = False
            for i, p_row in enumerate(self.notes):
                for j, p_col in enumerate(p_row):
                    if len(p_col) == 1:
                        self.guesses[i][j] = p_col[0]
                        self.no_given_locations.remove((i, j))
                        simplified_success = True
            self.notes = self._create_notes()
            self.calculate_possibilities()

    def _find_empty(self):
        """Finds empty cells in the grid."""
        for i in range(9):
            for j in range(9):
                if self.guess_at(i, j) == 0:
                    return i, j  # row, col
        return None

    def _solve_algorithm(self):
        """Uses a backtracking algorithm to solve the puzzle.

        Adapted from
        https://www.techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/
        """
        find = self._find_empty()
        if not find:
            return True
        else:
            row, col = find
        for i in range(1, 10):
            if not self.is_number_duplicate(row, col, i):
                self.guesses[row][col] = i
                if self._solve_algorithm():
                    return True
                self.guesses[row][col] = 0
        return False

    def solve(self) -> None:
        """Solves the puzzle."""
        self.calculate_possibilities()
        self.guess_simple_possibilities()
        self._solve_algorithm()


class GridGenerator(BaseGrid):
    """Generates a Sudoku grid.

    Code adapted from https://stackoverflow.com/a/56581709
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def _board_pattern(row, col) -> int:
        """Returns 012345678 for each row, shifted right one digit each row down.

        Apparently, using a board like this as a template only allows generation of
        a subset of the whole solution space but ehhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
        """
        return (3 * (row % 3) + row // 3 + col) % 9

    @staticmethod
    def _shuffle(iterable):
        """Returns a shuffled version of the supplied iterable."""
        return sample(iterable, len(iterable))

    def _generate_full_board(self):
        """Generates a full sudoku board and stores it in self.guesses."""
        number_range = range(3)
        rows = [g * 3 + r for g in self._shuffle(number_range) for r in self._shuffle(number_range)]
        cols = [g * 3 + c for g in self._shuffle(number_range) for c in self._shuffle(number_range)]
        numbers = range(1, 10)

        # produce board using randomized baseline pattern
        self.guesses = [[numbers[self._board_pattern(r, c)] for c in cols] for r in rows]

    def _remove_numbers(self, givens: int) -> None:
        """Removes numbers from the grid while maintaining validity."""
        filled_cells = 9 ** 2
        removed_cells = []
        solver = GridSolver()
        while filled_cells > givens:
            # yikes this is inefficient
            row = randint(0, 8)
            col = randint(0, 8)
            if (row, col) not in removed_cells:
                temp = self.guesses[row][col]
                self.guesses[row][col] = 0
                solver.reset()
                solver.setup(self.get_number_str())
                solver.solve()
                if not solver.sudoku_complete():
                    self.guesses[row][col] = temp
                else:
                    filled_cells -= 1

    def generate(self, givens: int) -> Tuple[str, str]:
        """Generates a new game board and returns the unsolved and solved number strings."""
        assert givens >= 17  # minimum no. of givens for solvable sudoku
        self.reset()
        self._generate_full_board()
        solved_number_str = self.get_number_str()
        self._remove_numbers(givens)
        return self.get_number_str(), solved_number_str


class GridModel(BaseGrid):
    """Models the game grid."""

    def __init__(self, number_str: str):
        super().__init__()
        self.setup(number_str)

    def _remove_guess_at_cell(self, row, col) -> None:
        """Clears guesses for the specified cell."""
        self.guesses[row][col] = 0

    def _remove_notes_at_cell(self, row, col) -> None:
        """Clears notes for the specified cell."""
        self.notes[row][col].clear()

    def clear_cell(self, row, col) -> None:
        """Clears guesses and notes for the specified cell."""
        self._remove_guess_at_cell(row, col)
        self._remove_notes_at_cell(row, col)

    def _remove_one_note(self, row, col, num) -> None:
        """Removes a note from the specified cell. Does not check whether `num` is in notes."""
        self.notes[row][col].remove(num)

    def _add_one_note(self, row, col, num) -> None:
        """Adds a note to the specified cell."""
        self.notes[row][col].append(num)

    def toggle_note(self, row, col, num) -> None:
        """Toggles a note at the specified position."""
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
        """Helper function to change the guess at the supplied position to `num`."""
        self.guesses[row][col] = num

    def toggle_guess(self, row, col, num) -> None:
        """Toggles a guess at the specified position."""
        if (row, col) not in self.given_locations:
            if self.guess_at(row, col) == num:
                self._remove_guess_at_cell(row, col)
            else:
                if self.notes_at(row, col):
                    self.notes[row][col].clear()
                self._add_guess(row, col, num)
                self._remove_notes_for_guess(row, col, num)


class GridView(tk.Canvas):
    """Draws the game grid."""

    GUESS_FONT = ("Arial", 20)
    GIVEN_FONT = ("Arial", 20)
    NOTE_FONT = ("Courier New", 14)

    def __init__(self, master, grid_size: int, board_width: int = 600, *args, **kwargs):
        super().__init__(master, bg="white", width=board_width, height=board_width, *args, **kwargs)
        self._master = master
        self._grid_size = grid_size
        self._board_width = board_width
        self._cell_length = board_width // grid_size

        self._BORDER_WIDTH = 1
        self._DIVIDER_THICKNESS = 4
        self._DIVIDER_POS = (  # hard-code time :sunglasses:
            ((0, 3), (8, 3)), ((0, 6), (8, 6)),
            ((3, 0), (3, 8)), ((6, 0), (6, 8))
        )

        self._selected_row = None
        self._selected_col = None

    @staticmethod
    def notes_to_str(notes: List[int]) -> str:
        """Converts a list of notes to a formatted string for display."""
        note_str = []
        for i in range(1, 10):
            if i != 1 and i % 3 == 1:
                note_str.append("\n")
            if i in notes:
                note_str.append(str(i))
            else:
                note_str.append(" ")
        return "".join(note_str)

    def set_selected_cell(self, pos: OptPosition) -> None:
        """Selects the cell at the position given."""
        self._selected_row, self._selected_col = pos

    def get_selected_cell(self) -> OptPosition:
        """Gets the position of the currently selected cell."""
        return self._selected_row, self._selected_col

    def check_valid_pixel_position(self, pixel: Pixel) -> None:
        """Checks whether the pixel supplied is within the board."""
        pixel_x, pixel_y = pixel
        if max(pixel_x, pixel_y) >= self._board_width or min(pixel_x, pixel_y) < 0:
            raise ValueError

    def pixel_to_position(self, pixel: Pixel) -> Position:
        """Converts a pixel location within the board to the position of the cell it is inside."""
        self.check_valid_pixel_position(pixel)
        pixel_x, pixel_y = pixel
        row = pixel_y // self._cell_length
        column = pixel_x // self._cell_length
        return row, column

    def _get_corner_coordinate(self, cell_position: Position, corner: str) -> Pixel:
        """Returns the coordinate of one of the corners of a cell."""
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
        """Returns the coordinate at the centre of a cell."""
        row, column = position
        pixel_x = floor((column + 0.5) * self._cell_length)
        pixel_y = floor((row + 0.5) * self._cell_length)
        return pixel_x, pixel_y

    def _draw_one_cell(self, position: Position) -> None:
        """Draws one square cell in the board."""
        top_left_x, top_left_y = self._get_corner_coordinate(position, "UP-LEFT")
        bottom_right_x, bottom_right_y = self._get_corner_coordinate(position, "DOWN-RIGHT")

        self.create_rectangle(
            top_left_x, top_left_y, bottom_right_x, bottom_right_y,
            fill="white" if position == self.get_selected_cell() else "light grey",
            outline="orange" if position == self.get_selected_cell() else "black",
            width=self._BORDER_WIDTH
        )

    def _draw_guess(self, position: Position, number: int) -> None:
        """Draws a guessed number."""
        text_x, text_y = self._get_centre_coordinate(position)
        self.create_text(text_x, text_y, anchor=tk.CENTER, font=self.GUESS_FONT, text=str(number))

    def _draw_given(self, position: Position, number: int) -> None:
        """Draws a given number."""
        text_x, text_y = self._get_centre_coordinate(position)
        self.create_text(
            text_x, text_y, anchor=tk.CENTER, fill="blue", font=self.GIVEN_FONT, text=str(number)
        )

    def _draw_notes(self, position: Position, notes: List[int]) -> None:
        """Draws a note. Monospaced font used to maintain spacing."""
        note_text = self.notes_to_str(notes)
        text_x, text_y = self._get_centre_coordinate(position)
        self.create_text(text_x, text_y, anchor=tk.CENTER, font=self.NOTE_FONT, text=note_text)

    def _draw_dividers(self) -> None:
        """Draws thick divider lines to separate the board into 3x3 squares."""
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
        """Draws the entire grid."""
        self.delete(tk.ALL)
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
        """Updates the button's appearance."""
        current_state = self._state_var.get()
        self.config(bg="light grey" if current_state else "SystemButtonFace")

    def _reverse_state(self) -> None:
        """Reverses the toggle state."""
        current_state = self._state_var.get()
        self._state_var.set(not current_state)
        # self._update_appearance()  # uncomment this if colour doesn't change, and report bug


class StopwatchFrame(tk.Frame):
    """Keeps time and displays it on the status bar."""

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
        """Returns a string converting the amount of seconds into minutes and seconds."""
        return f"{seconds // 60}m {seconds % 60:02d}s"

    def set_time(self, seconds: int) -> None:
        """Sets the current time recorded to `seconds`. Does not start the timer."""
        # Multiple after_ids need to be tracked to avoid weird timer behaviour
        # in the first few seconds after the timer is started.
        for after_id in self._after_ids:
            self.after_cancel(after_id)
        self._after_ids = []
        self._current_time = seconds
        self._update_labels()

    def start_timing(self) -> None:
        """Starts recording the time."""
        if not self._is_timing:
            self._is_timing = True
            self.after(1000, self._update_time)

    def stop_timing(self) -> None:
        """Stops recording the time."""
        self._is_timing = False

    def get_time(self) -> int:
        """Returns the recorded time in seconds."""
        return self._current_time

    def _update_time(self) -> None:
        """Increments the current time every second as long as self._is_timing == True."""
        for after_id in self._after_ids:
            self.after_cancel(after_id)
        self._after_ids = []
        if self._is_timing:
            self._current_time += 1
            self._update_labels()
            new_after_id = self.after(1000, self._update_time)
            self._after_ids.append(new_after_id)

    def _update_labels(self) -> None:
        """Update the time reading on the labels."""
        self._time_display_label.config(text=self.format_time(self._current_time))


class SudokuController(object):
    """Controller class for Sudoku app."""
    DEFAULT_GIVENS = 50
    HELP_TEXT = \
        """\
        Click on cell to select, esc to deselect
        Numbers 1-9 to input number
        Backspace/delete to remove number
        n to toggle between note and guess mode
        Arrow keys to move selected cell around
        g for new game
        h for this help information
        t for hint
        """

    def __init__(self, master: tk.Tk) -> None:
        """Constructs all game elements and widgets."""
        self._master = master
        self._outer_frame = tk.Frame(self._master)
        self._outer_frame.pack(side=tk.TOP)

        # top frame
        self._top_frame = tk.Frame(self._outer_frame)
        self._top_frame.pack(side=tk.TOP, expand=True, fill=tk.X)
        self._sudoku_label = tk.Label(self._top_frame, text="Sudoku", font=("Arial", 18))
        self._sudoku_label.pack(side=tk.LEFT, expand=True)
        self._timer = StopwatchFrame(self._top_frame, 0)
        self._timer.pack(side=tk.LEFT, expand=True)
        self._newgame_button = tk.Button(self._top_frame, text="New Game",
                                         command=self.new_game_dialog)
        self._newgame_button.pack(side=tk.LEFT, expand=True)

        # generation and grid
        self._note_mode = tk.BooleanVar()
        self._note_mode.set(False)

        self._generator = GridGenerator()
        self._solver = GridSolver()

        self._grid = None
        self._solved_grid_number_str = None
        self._new_game(self.DEFAULT_GIVENS)

        # view and binds
        self._view = GridView(self._outer_frame, 9, 630)
        self.create_binds()
        self._view.pack(side=tk.TOP, anchor=tk.N)

        # bottom frame
        self._bottom_frame = tk.Frame(self._outer_frame)
        self._bottom_frame.pack(side=tk.TOP, expand=True, fill=tk.X)
        self._controls_button = tk.Button(
            self._bottom_frame, text="Controls", command=self.controls_help
        )
        self._controls_button.pack(side=tk.LEFT, expand=True)
        self._note_button = ToggleButton(self._bottom_frame, self._note_mode, text="Note Mode")
        self._note_button.pack(side=tk.LEFT, expand=True)
        self._clear_cell_button = tk.Button(
            self._bottom_frame, text="Clear Cell", command=self.backspace
        )
        self._clear_cell_button.pack(side=tk.LEFT, expand=True)
        self._hint_button = tk.Button(
            self._bottom_frame, text="Get Hint", command=self.get_hint
        )
        self._hint_button.pack(side=tk.LEFT, expand=True)
        self._free_input_button = tk.Button(
            self._bottom_frame, text="Free Input", command=self._new_free_input_game
        )
        self._free_input_button.pack(side=tk.LEFT, expand=True)

        # draw the board to finish off
        self.redraw()
        self.game_has_finished = False

    def create_binds(self) -> None:
        """Makes binds for mouse and keyboard events. Only called during init."""
        def bind_helper(num):
            """Helps to bind number key presses using lambdas."""
            return lambda e: self.number_press(num)

        self._view.bind("<Button-1>", self.left_click)
        for i in range(1, 10):
            self._master.bind(str(i), bind_helper(i))

        self._master.bind("<BackSpace>", lambda e: self.backspace())
        self._master.bind("<Escape>", lambda e: self.escape())
        self._master.bind("n", lambda e: self.toggle_note_mode())
        self._master.bind("<Left>", lambda e: self.arrow("L"))
        self._master.bind("<Right>", lambda e: self.arrow("R"))
        self._master.bind("<Up>", lambda e: self.arrow("U"))
        self._master.bind("<Down>", lambda e: self.arrow("D"))
        self._master.bind("g", lambda e: self.new_game_dialog())
        self._master.bind("h", lambda e: self.controls_help())
        self._master.bind("t", lambda e: self.get_hint())

    def redraw(self) -> None:
        """Redraws the board."""
        self._view.draw_grid(self._grid.guesses, self._grid.notes, self._grid.given_locations)

    def left_click(self, event) -> None:
        """Handles left clicks on the board."""
        try:
            clicked_cell = self._view.pixel_to_position((event.x, event.y))
        except ValueError:
            return None
        if clicked_cell != self._view.get_selected_cell():
            self._view.set_selected_cell(clicked_cell)
        else:
            self._view.set_selected_cell((None, None))
        self.redraw()

    def arrow(self, direction: str) -> None:
        """Handles arrow key presses."""
        selected_cell = self._view.get_selected_cell()
        if selected_cell == (None, None):
            self._view.set_selected_cell((0, 0))
        else:
            row, col = selected_cell
            if direction == "L" and col > 0:
                col -= 1
            elif direction == "R" and col < 8:
                col += 1
            elif direction == "U" and row > 0:
                row -= 1
            elif direction == "D" and row < 8:
                row += 1
            self._view.set_selected_cell((row, col))
        self.redraw()

    def backspace(self) -> None:
        """Handles backspace key press."""
        selected_cell = self._view.get_selected_cell()
        if selected_cell != (None, None) and selected_cell not in self._grid.given_locations:
            self._grid.clear_cell(*selected_cell)
            self.redraw()

    def escape(self) -> None:
        """Handles escape key press."""
        self._view.set_selected_cell((None, None))
        self.redraw()

    def toggle_note_mode(self) -> None:
        """Toggles note mode."""
        self._note_mode.set(not self._note_mode.get())

    def number_press(self, number: int) -> None:
        """Handles a press of the number keys 1 through 9 (not on numeric keypad)."""
        cell = self._view.get_selected_cell()
        if cell != (None, None):
            if self._note_mode.get():
                self._grid.toggle_note(*self._view.get_selected_cell(), number)
            else:
                self._grid.toggle_guess(*self._view.get_selected_cell(), number)
            self.redraw()
            self.check_valid()

    def controls_help(self) -> None:
        """Displays a dialog box with information on game controls."""
        messagebox.showinfo(
            "Controls",
            self.HELP_TEXT
        )

    def get_hint(self) -> None:
        """Adds a new hint to the board, marking it as a given."""
        grid_number_str = self._grid.get_number_str()
        zeroes = [index for index, char in enumerate(grid_number_str) if char == "0"]
        if not zeroes:
            return None
        hint_index = choice(zeroes)
        row = hint_index // 9
        col = hint_index % 9
        self._grid.toggle_guess(row, col, self._solved_grid_number_str[hint_index])
        self._grid.given_locations.append((row, col))
        self._grid.no_given_locations.remove((row, col))
        self.redraw()
        self.check_valid()

    def new_game_dialog(self) -> None:
        """Asks the player how many given cells they would like in the new game."""
        self._timer.stop_timing()
        givens = simpledialog.askinteger("New Game", "Enter in number of given cells")
        givens = givens if givens else -1  # if dialog returns None, givens = -1
        if 17 <= givens <= 80:
            self._new_game(givens)
            self.redraw()
        else:
            messagebox.showerror("oops", "Given cell amount must be between 17 and 80.")
            if not self.game_has_finished:
                self._timer.start_timing()

    def _new_game(self, givens: int, free_input: bool = False) -> None:
        """Actually generates the new game."""
        self._timer.set_time(0)

        if free_input:
            generated_number_str = "0" * 81
            solved_number_str = "0" * 81
        else:
            generated_number_str, solved_number_str = self._generator.generate(givens)

        self._grid = GridModel(generated_number_str)
        self._solved_grid_number_str = solved_number_str

        self._timer.start_timing()
        self.game_has_finished = False

    def _new_free_input_game(self) -> None:
        """Clears the board and starts the game in free input mode."""
        self._timer.set_time(0)

        generated_number_str = "0" * 81
        solved_number_str = "0" * 81

        self._grid = GridModel(generated_number_str)
        self._solved_grid_number_str = solved_number_str
        self._timer.start_timing()
        self.game_has_finished = False

        self.redraw()        

    def check_valid(self) -> None:
        """Helper function to check if the grid is valid."""
        if self._grid.sudoku_complete():
            self.stop_game()

    def stop_game(self) -> None:
        """Stops the game."""
        self.game_has_finished = True
        self._timer.stop_timing()
        finish_time = self._timer.format_time(self._timer.get_time())
        messagebox.showinfo(title=f"nice", message=f"gj, you took {finish_time}!")


class SudokuApp(object):
    """Manages master window and controller class."""

    def __init__(self, master: tk.Tk) -> None:
        self._master = master
        self.controller = SudokuController(self._master)


def main():
    root = tk.Tk()
    _ = SudokuApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
