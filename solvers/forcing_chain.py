from grid import Grid
from utils import update_pygame, fill_hidden_singles, fill_naked_singles
from solver import solve
import csv


def count_fill_changes(grid, cell, value):
    """Counts the number of immediate changes in the grid by setting the cell to the given value"""
    grid_copy = grid.copy()
    grid_copy.fill(grid_copy.board[cell.row, cell.col], value)
    fill_hidden_singles(grid_copy)
    fill_naked_singles(grid_copy)

    return grid.count_differences(grid_copy)


def count_erase_changes(grid, cell, value):
    """Counts the number of immediate changes in the grid by removing the given value from the cell's candidates"""
    grid_copy = grid.copy()
    candidates = grid_copy.board[cell.row, cell.col].candidates
    if value in candidates:
        candidates.remove(value)
    fill_hidden_singles(grid_copy)
    fill_naked_singles(grid_copy)

    return grid.count_differences(grid_copy)


def complete_forcing_chain(grid: Grid, display=None, alpha=1):
    """Completes a forcing chain recursively starting with the given cell until
    it solves the puzzle (returns True), encounters a contradiction (returns False),
    or stalls (starts a new chain and returns the result).
    If there are not enough rounds of changes (given by alpha), it returns False"""

    # Fill singles
    changes = 1
    iterations = 0
    while changes > 0:
        grid_before = grid.copy()
        fill_hidden_singles(grid)
        fill_naked_singles(grid)
        changes = grid.count_differences(grid_before)
        if display:
            continue_ = update_pygame(display, grid)
            if not continue_:
                return None, False
        iterations += 1

    # Solved
    if grid.check_solved():
        return grid, True

    # Contradiction
    if not grid.check_valid():
        return grid, False

    # Stall

    # larger alpha prevents long rabbit holes
    # but removes comprehensiveness
    if iterations <= alpha:
        return grid, False

    return solve_forcing_chain(grid, display=display, alpha=alpha)


def solve_forcing_chain(grid, display=None, alpha=1):
    """Starts a backtracking algorithm by using a forcing chain on each cell until it solves th puzzle"""

    all_options = []
    for cell in grid.cells:
        if cell.correct:
            continue
        for candidate in cell.candidates:
            all_options.append((cell, candidate))

    # Sorts by candidates with greater effect
    all_options.sort(key=lambda x: count_fill_changes(grid, x[0], x[1]) + count_erase_changes(grid, x[0], x[1]),
                     reverse=True)

    for cell, value in all_options:
        grid_copy = grid.copy()
        cell_copy = cell.copy()
        grid_copy.fill(cell_copy, value)
        if not grid_copy.check_valid_cell(cell):
            continue
        new_grid, solved = complete_forcing_chain(grid_copy, display=display, alpha=alpha)
        if new_grid is None:
            return None, False
        if solved:
            return new_grid, True
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
    solve(examples_easy, solve_forcing_chain)
    solve(example_hard, solve_forcing_chain)
