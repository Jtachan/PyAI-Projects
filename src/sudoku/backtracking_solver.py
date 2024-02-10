"""
Here is contained all codes to solve a sudoku using backtracking
"""
import numpy as np

from sudoku import Sudoku


class UnsolvableSudoku(ValueError):
    """Error for when the sudoku cannot be solved"""


class SudokuBackTrkSolver:
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
        self._board = np.array(sudoku.board)
        self._max_digit = sudoku.size
        self._height = height
        self._width = width

    def _is_valid_guess(self, guess: int, tile_row: int, tile_col: int) -> bool:
        """
        Checks if a number is valid for the given coordinates. A valid guess is any
        number not contained in the row, column or major tile.

        Parameters
        ----------

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
        2. A guess is made and checked to be valid for the coordinates.
        """
        try:
            row_idx, col_idx = np.array(np.where(self._board == None)).T[0]
        except IndexError:
            # No more empty places at the board
            return True

        for guess in range(1, self._max_digit + 1):
            if self._is_valid_guess(guess=guess, tile_row=row_idx, tile_col=col_idx):
                self._board[row_idx, col_idx] = guess

                if self._backtracking():
                    return True

                # Backtracking all the guesses until the initial one
                self._board[row_idx, col_idx] = None

        return False

    def solve(self):
        """Solves the sudoku and prints the solution"""
        print(
            "Initial state:\n"
            f"{np.where(self._board == None, 'x', self._board.astype(str))}\n"
        )
        if not self._backtracking():
            raise UnsolvableSudoku("The given sudoku doesn't have a solution")
        print(f"Solution:\n{self}")

    def __str__(self):
        return str(self._board.astype(str))


if __name__ == "__main__":
    solver = SudokuBackTrkSolver(difficulty=0.9)
    solver.solve()
