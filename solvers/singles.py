from solvers.forcing_chain import fill_naked_singles, fill_hidden_singles
from utils import update_pygame
from solver import solve
import csv


def solve_sinlges(grid, display=None):
    while not grid.check_solved():
        grid_before = grid.copy()
        fill_naked_singles(grid)
        fill_hidden_singles(grid)
        if grid.count_differences(grid_before) == 0:
            return grid, False
        continue_ = update_pygame(display, grid)
        if not continue_:
            return None, False
    return grid, True


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
    solve(examples_easy, solve_sinlges)
    solve(example_hard, solve_sinlges)
