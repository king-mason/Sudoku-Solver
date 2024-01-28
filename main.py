from solver import solve
from config import (WIDTH, HEIGHT, BG_COLOR, DELAY)
import csv
from solvers.combined_solver import solve_combined



delay = DELAY
DISPLAY_SOLVER = True


if __name__ == '__main__':

    example_hard_boards = []
    example_easy_boards = []
    with open('datasets/reglib-1.3.txt') as file:
        for line in file:
            if line[0] != ':':
                continue
            info = line.strip().split(':')
            givens = info[3]
            code = ''
            skip = False
            for char in givens:
                if skip:
                    code += '.'
                    skip = False
                elif char == '+':
                    skip = True
                else:
                    code += char

            optional_code = givens.replace('+', '')

            example_hard_boards.append(code)
            example_easy_boards.append(optional_code)

    examples = []
    solutions = []
    with open('datasets/sudoku.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            examples.append(row['quizzes'])
            solutions.append(row['solutions'])

    examples = example_hard_boards[:]

    # examples = ['9..8...........5............2..1...3.1.....6....4...7.7.86.........3.1..4.....2..']
    # examples = ['6....3..7....4..6..54867..........1.162.8.749.3..........42193..1..7....4..6....5']
    solve(examples, solve_combined)
