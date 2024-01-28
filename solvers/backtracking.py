from utils import update_pygame
from solver import solve
import random
import csv


def solve_backtracking(grid, display=None):
    # Test for base case
    for i in range(81):
        cell = grid.board[i // 9, i % 9]
        if cell.value == 0:
            break
    else:
        # all squares filled
        return grid, True

    for i in range(1, 10):
        cell.value = i
        if not grid.check_valid_cell(cell):
            continue

        if display:
            continue_ = update_pygame(display, grid)
            if not continue_:
                return None, False

        new_grid, solved = solve_backtracking(grid, display)

        if new_grid is None:
            return None, False
        if solved:
            return new_grid, True
    cell.value = 0
    return grid, False


def solve_random_backtracking(grid, display=None):
    # Test for base case
    for i in range(81):
        cell = grid.board[i // 9, i % 9]
        if cell.value == 0:
            break
    else:
        # all squares filled
        return grid, True

    used = set()
    while cell.candidates - used:
        cell.value = random.choice(list(cell.candidates - used))
        if not grid.check_valid_cell(cell):
            used.add(cell.value)
            continue

        if display:
            continue_ = update_pygame(display, grid)
            if not continue_:
                return None, False

        new_grid, solved = solve_random_backtracking(grid, display)

        if new_grid is None:
            return None, False
        if solved:
            return new_grid, True
        used.add(cell.value)
    cell.value = 0
    return grid, False


if __name__ == '__main__':

    # load 10 examples
    examples_easy = []
    with open('../datasets/sudoku.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in list(reader)[:10]:
            examples_easy.append(row['quizzes'])
    # load hard example
    example_hard = ['9..8...........5............2..1...3.1.....6....4...7.7.86.........3.1..4.....2..']

    # test
    solve(examples_easy, solve_backtracking)
    solve(example_hard, solve_backtracking)
