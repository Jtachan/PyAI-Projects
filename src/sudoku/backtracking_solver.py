"""
Here is contained all codes to solve a sudoku using backtracking
"""
import numpy as np

from sudoku import Sudoku


class UnsolvableSudoku(ValueError):
    """Error for when the sudoku cannot be solved"""


class BacktrackingSolver:
    """Class to solve a sudoku puzzle using backtracking"""

    def __init__(self, width: int = 3, height: int = 3, difficulty: float = 0.3):
        """
        Initializes the solver, generating a sudoku with it.

        Parameters
        ----------
        width : int
            Number of horizontal cells contained in a major cell.
        height : int
            Number of vertical cells contained in a major cell.
        difficulty : float
            Difficulty level for the sudoku, defining the percentage of cells that
            won't contain digits.
        """
        sudoku = Sudoku(width=width, height=height).difficulty(difficulty)
        self._board = np.array(
            [
                [digit if digit is not None else 0 for digit in row]
                for row in sudoku.board
            ]
        )
        self._max_digit = sudoku.size
        self._height = height
        self._width = width
        self._max_digit = height * width

    def _is_valid_guess(self, guess: int, tile_row: int, tile_col: int) -> bool:
        """
        Checks if a number is valid for the given coordinates. A valid guess is any
        number not contained in the row, column or major tile.

        Parameters
        ----------
        guess: int
            Number to be checked.
        tile_row : int
            Row coordinate in which the tile is positioned.
        tile_col : int
            Column coordinate in which the tile is positioned.

        Returns
        -------
        bool :
            Whether the guess is valid.
        """
        # Guess not contained in the row or the column
        row, col = self._board[tile_row], self._board[..., tile_col]
        if guess in row or guess in col:
            return False

        # Guess not contained in its major tile
        row_start = (tile_row // self._width) * self._width
        col_start = (tile_col // self._height) * self._height
        for row_idx in range(row_start, row_start + self._width):
            for col_idx in range(col_start, col_start + self._height):
                if self._board[row_idx, col_idx] == guess:
                    return False

        return True

    def _backtracking(self) -> bool:
        """
        Backtracking algorithm to solve the sudoku.

        Returns
        -------
        bool:
            Whether the sudoku is solved for the latest guess.

        Algorithm Details
        -----------------
        1. An empty space is searched for within the board. Only if the board is solved
           there won't be any.
        2. A guess is made and checked to be valid for the coordinates (empty space).
        3. With a valid guess, the algorithm calls itself recursively repeating
           previous steps.
        4. If any guess was not the correct number, the guesses are deleted until the
           last one in which there were at least one possible guess left.
        5. The algorithm continues until the puzzle is solved or the puzzle is found
           to be unsolvable.
        """
        try:
            row_idx, col_idx = np.array(np.where(self._board == 0)).T[0]
        except IndexError:
            # No more empty places at the board
            return True

        for guess in range(1, self._max_digit + 1):
            if self._is_valid_guess(guess=guess, tile_row=row_idx, tile_col=col_idx):
                self._board[row_idx, col_idx] = guess

                if self._backtracking():
                    return True

                # Backtracking all the guesses until the initial one
                self._board[row_idx, col_idx] = 0

        return False

    def solve(self):
        """Solves the sudoku and prints the solution"""
        print(f"Initial state\n{self}")
        if not self._backtracking():
            raise UnsolvableSudoku("The given sudoku doesn't have a solution")
        print(f"Solution\n{self}")

    def __str__(self):
        board_repr = ""
        hline = "-" * (self._width * 2 + 1) * self._width + "\n"
        board_1d_size = self._board.shape[0]

        for row_idx in range(board_1d_size):
            if row_idx % self._height == 0:
                board_repr += hline

            for col_idx in range(board_1d_size):
                digit = self._board[row_idx, col_idx]

                board_repr += f"{digit} " if digit != 0 else "  "
                if col_idx == (board_1d_size - 1):
                    board_repr += "\n"
                elif (col_idx + 1) % self._width == 0:
                    board_repr += "| "
        board_repr += hline

        return board_repr


if __name__ == "__main__":
    solver = BacktrackingSolver()
    solver.solve()
