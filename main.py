import numpy as np
import math
import sys
import random
import copy

# u'\u25a1'

class queen:
    def __init__(self, i, j):
        super().__init__()
        self.position = [i, j]
        self.cost_board = [[0 for i in range(0, 8)] for j in range(0, 8)]
        self.totalViolationsRow = 0
        self.totalViolationsDiagonal = 0
        self.total_violations = self.totalViolationsRow + self.totalViolationsDiagonal
queen_list = []

class board:
    def __init__(self):
        super().__init__()
        self.board = [[ " " for i in range(0, 8)] for j in range(0, 8)]
        self.board_violations = 0

    """
        Add queen to random spot on board (cannot be a column where a Queen exists already)
    """
    def __add_queen__(self):
        self.board_violations = 0
        i = random.randint(0,7)
        j = random.randint(0,7)
        if(self.__column_check__(j)):
            self.board[i][j] = "Q"
            queen_list.append(queen(i, j))
            queen_list.sort(key=lambda x:x.position[1])
        else:
            return self.__add_queen__()


    """
        Check amount of violations for each queen on the board (returns sum of all violations)
    """
    def __check_violations_on_board__(self):
        total_board_violations = 0
        for queen in queen_list:
            total_board_violations += self.__update_current_queen_violations__(queen)
        self.board_violations = (total_board_violations / 2)
        print("Current Board Violations: ", self.board_violations)
        return self.board_violations

    """
        Check current violations for given queen on the current spot
        updates queen.total_violations
    """
    def __update_current_queen_violations__(self, queen):
        currentQueenRow = queen.position[0]
        currentQueenColumn = queen.position[1]
        totalViolationsRow = 0

        #check row
        for column in range(8):
            if (column == currentQueenColumn):
                continue
            if (self.board[currentQueenRow][column] == "Q"):
                totalViolationsRow = totalViolationsRow + 1
        queen.totalViolationsRow = totalViolationsRow

        #         check diagonal
        major = (np.diagonal(np.array(self.board), offset=(currentQueenColumn - currentQueenRow)))
        minor = (np.diagonal(np.rot90(np.array(self.board)), offset=-np.array(self.board).shape[1] + (currentQueenColumn + currentQueenRow) + 1))
        queen.totalViolationsDiagonal = math.ceil(( (np.count_nonzero(major == "Q") - 1) + (np.count_nonzero(minor == "Q")-1) ))
        queen.total_violations = queen.totalViolationsDiagonal + queen.totalViolationsRow
        return queen.total_violations


    """
        Simulates the queen going to a certain spot
        get the amount of violations that it would have there
        returns a cost board with each spot having the violations amount for the queen there
    """
    def __check_all_possible_violations_of_queen__(self, queen):
        original_row = queen.position[0]
        original_column = queen.position[1]
        cost_board = copy.deepcopy(self.board)
        currentTotalViolations = queen.total_violations

        #reseting original queen
        cost_board[original_row][original_column] = " "
        
        #testing every possible move in the column
        for i in range(8):
            cost_array = []
            future_position_violation = 0

            #COLUMNS CHECK
            for column in range(8):
                if (column == original_column):
                    continue
                if (cost_board[i][column] == "Q"):
                    future_position_violation = future_position_violation + 1
            

            #DIAGONAL CHECK
            cost_board_lst = np.array(cost_board)
            major = (np.diagonal(cost_board_lst, offset=(original_column - i)))
            minor = (np.diagonal(np.rot90(cost_board_lst), offset=-cost_board_lst.shape[1] + (original_column + i) + 1))

            #list(major).count("Q") + list(minor).count("Q")
            #(np.count_nonzero(major == "Q")) + (np.count_nonzero(minor == "Q"))

            future_position_violation = future_position_violation + list(major).count("Q") + list(minor).count("Q")

            cost_board[i][original_column] = future_position_violation
            cost_array.append(future_position_violation)

        cost_board[original_row][original_column] = "Q"
        return cost_board
    

    """
        Moves queen to lower violations spot
    """
    def __move_queen_to_lower_cost__(self, queen, cost_board):
        original_row = queen.position[0]
        original_column = queen.position[1]
        smallest_violations = sys.maxsize
        smallest_position = [original_row, original_column]

        if queen.total_violations == 0:
            return smallest_position, queen.total_violations

        for i in range(8):
            if (cost_board[i][original_column] != "Q") and (cost_board[i][original_column] <= smallest_violations) and (cost_board[i][original_column] <= queen.total_violations):
                smallest_violations = cost_board[i][original_column]
                smallest_position = [i, original_column]
        if smallest_violations == sys.maxsize:
            smallest_violations = queen.total_violations

        return smallest_position, smallest_violations

    def __hill_climbing__(self):
        print("Looking for better queen positions")
        for queen in queen_list:
            for update in queen_list:
                self.__update_current_queen_violations__(update)
            if queen.total_violations < 1:
                continue
            cost_board = copy.deepcopy(self.__check_all_possible_violations_of_queen__(queen))

            print("BEFORE CHANGE: ")
            print("Queen total current violations: ", queen.total_violations)
            print(np.matrix(cost_board))
            print("MOVE QUEEN TO LOWER COST")
            print("Queen total current violations: ", queen.total_violations)
            smallest_position, smallest_violations = self.__move_queen_to_lower_cost__(queen, cost_board)
            self.board[queen.position[0]][queen.position[1]] = " "

            #MOVED QUEEN UPDATE
            queen.position[0] = smallest_position[0]
            queen.position[1] = smallest_position[1]
            queen.total_violations = smallest_violations

            self.board[queen.position[0]][queen.position[1]] = "Q"
            print("AFTER CHANGE: ")
            print("Queen total current violations: ", queen.total_violations)
            print(np.matrix(self.board))

    def __column_check__(self, j):
        for i in range(8):
            if(self.board[i][j] == "Q"):
                return False
        return True


if __name__ == "__main__":
    b = board()
    for i in range(8):
        b.__add_queen__()
        print("After adding new queen Board Violations: ", b.__check_violations_on_board__())
        while b.__check_violations_on_board__() != 0:
            print(np.matrix(b.board))
            b.__hill_climbing__()
    print("FINAL MATRIX: ")
    print(np.matrix(b.board))
    b.__check_violations_on_board__()
    for queen in queen_list:
        print("Queen Position: ", queen.position)
        print("Queen Violations: ", queen.total_violations)
        print("----------------")

    with open("results.txt", "a") as resultsFile:
        resultsFile.write(np.array2string(np.matrix(b.board), formatter={'str_kind': lambda x: x}))
        resultsFile.write("\n\n\n")