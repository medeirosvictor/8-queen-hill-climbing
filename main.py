import numpy as np
import math
import sys
import random
import copy
from typing import List, Tuple

MAX_HILL_CLIMB_ITERATIONS = 100


class Queen:
    """Represents a single queen on the board with its position and violation counts."""

    def __init__(self, i: int, j: int) -> None:
        self.position: List[int] = [i, j]
        self.cost_board: List[List[int]] = [[0 for _ in range(8)] for _ in range(8)]
        self.totalViolationsRow: int = 0
        self.totalViolationsDiagonal: int = 0
        self.total_violations: int = 0


class Board:
    """8x8 chess board that places queens and solves conflicts via hill climbing."""

    def __init__(self) -> None:
        self.board: List[List[str]] = [[" " for _ in range(8)] for _ in range(8)]
        self.board_violations: float = 0
        self.queens: List[Queen] = []

    def add_queen(self) -> None:
        """Add a queen to a random row in a random available (empty) column."""
        self.board_violations = 0
        available_columns = [j for j in range(8) if self.column_is_free(j)]
        if not available_columns:
            return
        j = random.choice(available_columns)
        i = random.randint(0, 7)
        self.board[i][j] = "Q"
        self.queens.append(Queen(i, j))
        self.queens.sort(key=lambda x: x.position[1])

    def check_violations_on_board(self) -> float:
        """Return the total number of conflicts on the board (halved to avoid double-counting)."""
        total_board_violations = 0
        for q in self.queens:
            total_board_violations += self.update_queen_violations(q)
        self.board_violations = total_board_violations / 2
        print("Current Board Violations: ", self.board_violations)
        return self.board_violations

    def update_queen_violations(self, q: Queen) -> int:
        """Recompute and return the violation count for a single queen."""
        row = q.position[0]
        col = q.position[1]
        violations_row = 0

        # Check row
        for column in range(8):
            if column == col:
                continue
            if self.board[row][column] == "Q":
                violations_row += 1
        q.totalViolationsRow = violations_row

        # Check diagonals
        board_arr = np.array(self.board)
        major = np.diagonal(board_arr, offset=(col - row))
        minor = np.diagonal(
            np.rot90(board_arr),
            offset=-board_arr.shape[1] + (col + row) + 1,
        )
        q.totalViolationsDiagonal = math.ceil(
            (np.count_nonzero(major == "Q") - 1)
            + (np.count_nonzero(minor == "Q") - 1)
        )
        q.total_violations = q.totalViolationsDiagonal + q.totalViolationsRow
        return q.total_violations

    def compute_cost_board(self, q: Queen) -> List[List]:
        """Build a cost board showing the violation count for the queen at every row in its column.

        Simulates moving the queen to each row and counts the conflicts it would have there.
        The queen's current cell is marked with 'Q' while all other rows hold an integer cost.
        """
        original_row = q.position[0]
        original_column = q.position[1]
        cost_board = copy.deepcopy(self.board)

        # Temporarily remove the queen
        cost_board[original_row][original_column] = " "

        # Test every possible row in this column
        for i in range(8):
            future_violations = 0

            # Row conflicts
            for column in range(8):
                if column == original_column:
                    continue
                if cost_board[i][column] == "Q":
                    future_violations += 1

            # Diagonal conflicts
            cost_arr = np.array(cost_board)
            major = np.diagonal(cost_arr, offset=(original_column - i))
            minor = np.diagonal(
                np.rot90(cost_arr),
                offset=-cost_arr.shape[1] + (original_column + i) + 1,
            )
            future_violations += list(major).count("Q") + list(minor).count("Q")

            cost_board[i][original_column] = future_violations

        cost_board[original_row][original_column] = "Q"
        return cost_board

    def move_queen_to_lower_cost(
        self, q: Queen, cost_board: List[List]
    ) -> Tuple[List[int], int]:
        """Find the lowest-cost row for the queen in its column and return (position, cost).

        Only moves the queen if a position with fewer or equal violations exists.
        """
        original_row = q.position[0]
        original_column = q.position[1]
        smallest_violations = sys.maxsize
        smallest_position = [original_row, original_column]

        if q.total_violations == 0:
            return smallest_position, q.total_violations

        for i in range(8):
            cell = cost_board[i][original_column]
            if cell != "Q" and cell <= smallest_violations and cell <= q.total_violations:
                smallest_violations = cell
                smallest_position = [i, original_column]

        if smallest_violations == sys.maxsize:
            smallest_violations = q.total_violations

        return smallest_position, smallest_violations

    def hill_climb(self) -> None:
        """Run one pass of hill climbing: try to move every conflicted queen to a better row."""
        print("Looking for better queen positions")
        for q in self.queens:
            for update in self.queens:
                self.update_queen_violations(update)
            if q.total_violations < 1:
                continue
            cost_board = copy.deepcopy(self.compute_cost_board(q))

            print("BEFORE CHANGE: ")
            print("Queen total current violations: ", q.total_violations)
            print(np.matrix(cost_board))
            print("MOVE QUEEN TO LOWER COST")
            print("Queen total current violations: ", q.total_violations)
            smallest_position, smallest_violations = self.move_queen_to_lower_cost(
                q, cost_board
            )
            self.board[q.position[0]][q.position[1]] = " "

            # Move queen
            q.position[0] = smallest_position[0]
            q.position[1] = smallest_position[1]
            q.total_violations = smallest_violations

            self.board[q.position[0]][q.position[1]] = "Q"
            print("AFTER CHANGE: ")
            print("Queen total current violations: ", q.total_violations)
            print(np.matrix(self.board))

    def column_is_free(self, j: int) -> bool:
        """Return True if no queen occupies column j."""
        for i in range(8):
            if self.board[i][j] == "Q":
                return False
        return True


if __name__ == "__main__":
    b = Board()
    for i in range(8):
        b.add_queen()
        print(
            "After adding new queen Board Violations: ",
            b.check_violations_on_board(),
        )
        iterations = 0
        while b.check_violations_on_board() != 0:
            iterations += 1
            if iterations > MAX_HILL_CLIMB_ITERATIONS:
                print(
                    f"Hill climbing stuck after {MAX_HILL_CLIMB_ITERATIONS} iterations "
                    f"with {b.board_violations} violations remaining. "
                    "Performing random restart for this queen."
                )
                # Random restart: remove the last-placed queen and re-add it
                last_queen = b.queens[-1]
                b.board[last_queen.position[0]][last_queen.position[1]] = " "
                b.queens.pop()
                b.add_queen()
                iterations = 0
                continue
            print(np.matrix(b.board))
            b.hill_climb()

    print("FINAL MATRIX: ")
    print(np.matrix(b.board))
    b.check_violations_on_board()
    for q in b.queens:
        print("Queen Position: ", q.position)
        print("Queen Violations: ", q.total_violations)
        print("----------------")

    with open("results.txt", "a") as resultsFile:
        resultsFile.write(
            np.array2string(
                np.matrix(b.board), formatter={"str_kind": lambda x: x}
            )
        )
        resultsFile.write("\n\n\n")
