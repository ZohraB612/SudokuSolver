class SudokuSolver:
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def is_valid(self, row, col, num):
        # Check if the number is already present in the row
        if num in self.puzzle[row]:
            return False
        
        # Check if the number is already present in the column
        if num in [self.puzzle[i][col] for i in range(9)]:
            return False
        
        # Check if the number is already present in the 3x3 grid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.puzzle[i][j] == num:
                    return False
        
        return True

    def solve(self):
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid(i, j, num):
                            self.puzzle[i][j] = num
                            # Uncomment next line to print the current state of the puzzle at each step
                            # self.print_container()
                            if self.solve():
                                return True
                            self.puzzle[i][j] = 0
                    return False
        return True

    def print_container(self):
        print("\n".join([" ".join(map(str, row)) for row in self.puzzle]))


def create_sudoku():
    container = [
        [0, 0, 0, 0, 0, 8, 3, 0, 0],
        [0, 0, 0, 0, 2, 4, 0, 9, 0],
        [0, 0, 4, 0, 7, 0, 0, 0, 6],
        [0, 0, 0, 0, 0, 3, 0, 7, 9],
        [7, 5, 0, 0, 0, 0, 0, 8, 4],
        [9, 2, 0, 5, 0, 0, 0, 0, 0],
        [4, 0, 0, 0, 9, 0, 1, 0, 0],
        [0, 3, 0, 4, 6, 0, 0, 0, 0],
        [0, 0, 5, 8, 0, 0, 0, 0, 0]
    ]
    return container


if __name__ == "__main__":
    PUZZLE = create_sudoku()
    SUDOKU = SudokuSolver(PUZZLE)
    print("Original Puzzle:")
    SUDOKU.print_container()

    if SUDOKU.solve():
        print("\nSolved Puzzle:")
        SUDOKU.print_container()
    else:
        print("No solution exists.")
