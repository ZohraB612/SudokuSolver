import sqlite3

import sqlite3

# Establish connection and cursor
conn = sqlite3.connect('sudoku_puzzles.db')
cursor = conn.cursor()

# Create the 'puzzles' table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS puzzles
               (id INTEGER PRIMARY KEY,
               puzzle TEXT,
               solution TEXT)''')

# Commit the changes
conn.commit()

# Close the connection
conn.close()

class SudokuSolver:
    def __init__(self, puzzle=None):
        self.puzzle = puzzle or [[0]*9 for _ in range(9)]

    def is_valid(self, row, col, num):
        if num in self.puzzle[row]:
            return False
        
        if num in [self.puzzle[i][col] for i in range(9)]:
            return False
        
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.puzzle[i][j] == num:
                    return False
        
        return True

    def generate_solution(self):
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid(i, j, num):
                            self.puzzle[i][j] = num
                            if self.generate_solution():
                                return True
                            self.puzzle[i][j] = 0
                    return False
        return True

    def print_container(self):
        print("\n".join([" ".join(map(str, row)) for row in self.puzzle]))
        
    def input_custom(self):
        print("Enter your Sudoku puzzle row by row (use 0 for empty cells):")
        for i in range(9):
            row = list(map(int, input().split()))
            self.puzzle[i] = row

conn = sqlite3.connect('sudoku_puzzles.db')
cursor = conn.cursor()

def insert_puzzle(puzzle, solution):
    cursor.execute("INSERT INTO puzzles (puzzle, solution) VALUES (?, ?)", (puzzle, solution))
    conn.commit()

def get_puzzle_by_id(puzzle_id):
    cursor.execute("SELECT puzzle, solution FROM puzzles WHERE id=?", (puzzle_id,))
    return cursor.fetchone()

def get_all_puzzles():
    cursor.execute("SELECT * FROM puzzles")
    return cursor.fetchall()

def close_connection():
    conn.close()

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
    SUDOKU = SudokuSolver()
    print("Choose an option:")
    print("1. Solve a predefined puzzle")
    print("2. Input your own puzzle")
    print("3. List all puzzles")
    print("4. Retrieve a puzzle by ID")
    choice = input()

    if choice == '1':
        PUZZLE = create_sudoku()
        SUDOKU = SudokuSolver(PUZZLE)
        SUDOKU.generate_solution() 
        SUDOKU.print_container() 

    elif choice == '2':
        SUDOKU.input_custom()

        # Convert the user-input puzzle to a string for comparison
        user_puzzle_str = "\n".join(" ".join(map(str, row)) for row in SUDOKU.puzzle)

        # Check if the puzzle already exists in the database
        cursor.execute("SELECT id, solution FROM puzzles WHERE puzzle=?", (user_puzzle_str,))
        existing_puzzle = cursor.fetchone()

        if existing_puzzle:
            puzzle_id, solution_str = existing_puzzle
            print(f"This puzzle already exists in the database. Here is the solution (ID: {puzzle_id}):")
            print(solution_str)
        else:
            # Create a new puzzle using create_sudoku() to get the solution
            new_puzzle = create_sudoku()

            # Create a SudokuSolver instance for generating the solution
            solution_solver = SudokuSolver(SUDOKU.puzzle)
            solution_solver.generate_solution()
            solution = solution_solver.puzzle

            # Now, save the user input and the solution to the database
            puzzle_str = user_puzzle_str
            solution_str = "\n".join(" ".join(map(str, row)) for row in solution)
            insert_puzzle(puzzle_str, solution_str)

            # Print the solution
            print("\nSolution:")
            solution_solver.print_container()

    elif choice == '3':
        puzzles = get_all_puzzles()
        for puzzle in puzzles:
            print(f"ID: {puzzle[0]}, Puzzle: {puzzle[1]}, Solution: {puzzle[2]}")
    
    elif choice == '4':
        puzzle_id = input("Enter the ID of the puzzle you want to retrieve: ")
        puzzle = get_puzzle_by_id(puzzle_id)
        if puzzle:
            print(f"Puzzle: {puzzle[0]}\nSolution: {puzzle[1]}")
        else:
            print("Puzzle not found.")
    else:
        print("Invalid choice. Exiting...")

    close_connection()