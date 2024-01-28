from solvers.forcing_chain import solve_forcing_chain
from solvers.singles import solve_sinlges
from solver import solve
import csv


def solve_combined(grid, display=None):
    grid, success = solve_sinlges(grid, display)
    if grid is None:
        return None, False
    if success:
        return grid, True
    return solve_forcing_chain(grid, display)


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
    solve(examples_easy, solve_combined)
    solve(example_hard, solve_combined)
