import time

import pygame
from grid import Grid
from config import (WIDTH, HEIGHT, BG_COLOR, DELAY)
from utils import update_pygame, timer
import csv

delay = DELAY
DISPLAY_SOLVER = True


def solve(sudoku_list, solving_function):
    start_time = time.time()

    solved = []
    if DISPLAY_SOLVER:
        pygame.init()
        pygame.display.set_caption('Sudoku Solver')

        pygame.time.set_timer(timer, DELAY)

        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        screen.fill(BG_COLOR)
    else:
        screen = None

    for board in sudoku_list:
        grid = Grid(board)
        grid.fix_candidates()
        if DISPLAY_SOLVER:
            continue_ = update_pygame(screen, grid, num_solved=len(solved))
            if not continue_:
                return solved
        grid, success = solving_function(grid, screen)

        if grid is None:
            return solved

        if grid.check_solved():
            solved.append(grid)
        else:
            print('Unsolved:', board)

        if DISPLAY_SOLVER:
            continue_ = update_pygame(screen, grid, num_solved=len(solved))
            if not continue_:
                return solved
        elif len(solved) % 1000 == 0:
            print(len(solved))

    end_time = time.time()

    print('Solved all puzzles!')
    print(f'Program took {round(end_time - start_time, 8)} seconds')

    if DISPLAY_SOLVER:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or \
                            event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return solved

    return solved

