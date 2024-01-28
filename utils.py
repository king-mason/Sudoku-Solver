import pygame
from config import (WIDTH, HEIGHT, OUTLINE_COLOR, NUM_SIZE, BG_COLOR, DELAY)


timer = pygame.USEREVENT + 1


def fill_naked_singles(grid):
    for i in range(9):
        for j in range(9):
            cell = grid.board[i, j]
            if cell.correct:
                continue
            choices = list(cell.candidates)
            if len(choices) == 1:
                grid.fill(cell, choices[0])


def fill_hidden_singles(grid):
    # check rows
    for i in range(9):
        for j in range(9):
            cell = grid.board[i, j]
            if cell.correct:
                continue

            # check row
            seen_row = set()
            for other_cell in grid.scan_row(cell):
                if other_cell.correct:
                    continue
                for candidate in other_cell.candidates:
                    seen_row.add(candidate)

            # check column
            seen_col = set()
            for other_cell in grid.scan_col(cell):
                if other_cell.correct:
                    continue
                for candidate in other_cell.candidates:
                    seen_col.add(candidate)

            # check subgrid
            seen_subgrid = set()
            for other_cell in grid.scan_subgrid(cell):
                if other_cell.correct:
                    continue
                for candidate in other_cell.candidates:
                    seen_subgrid.add(candidate)

            # compare
            for candidate in cell.candidates:
                if candidate not in seen_row or candidate not in seen_col or candidate not in seen_subgrid:
                    grid.fill(cell, candidate)
                    break


def update_pygame(screen, grid, print_notes=True, num_solved=None):
    font_large = pygame.font.SysFont(pygame.font.get_default_font(), size=NUM_SIZE)
    font_small = pygame.font.SysFont(pygame.font.get_default_font(), size=25)
    screen.fill(BG_COLOR)

    # Draw outer rectangle
    outline_rect = pygame.rect.Rect(WIDTH // 16, 3 * HEIGHT // 32, WIDTH - WIDTH // 8, HEIGHT - HEIGHT // 8)
    outline_width = 5
    pygame.draw.rect(screen, OUTLINE_COLOR, outline_rect, width=outline_width)

    # Drawing lines
    for i in range(1, 9):
        if i % 3:
            outline_width = 2
        else:
            outline_width = 5
        pygame.draw.line(screen, OUTLINE_COLOR, (outline_rect.left + + outline_rect.width * i / 9, outline_rect.top),
                         (outline_rect.left + outline_rect.width * i / 9, outline_rect.bottom - 5),
                         width=outline_width)
        pygame.draw.line(screen, OUTLINE_COLOR, (outline_rect.left, outline_rect.top + outline_rect.width * i / 9),
                         (outline_rect.right - 5, outline_rect.top + outline_rect.width * i / 9),
                         width=outline_width)

    for i in range(9):
        for j in range(9):
            cell = grid.board[i, j]
            if cell.given:
                num_color = (0, 0, 0)
            else:
                num_color = (0, 75, 150)
            if cell.value == 0:
                if not print_notes:
                    continue
                for candidate in cell.candidates:
                    num_surf = font_small.render(str(candidate), False, num_color)
                    num_rect = num_surf.get_rect()
                    num_rect.center = (outline_rect.left + outline_rect.width * j / 9 +
                                       (((candidate - 1) % 3) + 1) * outline_rect.width / 36,
                                       outline_rect.top + outline_rect.height * i / 9 +
                                       (((candidate - 1) // 3) + 1) * outline_rect.height / 36)
                    screen.blit(num_surf, num_rect)
            else:
                num_surf = font_large.render(str(cell.value), False, num_color)
                num_rect = num_surf.get_rect()
                num_rect.center = (outline_rect.left + outline_rect.width * (2*j + 1) / 18,
                                   outline_rect.top + outline_rect.height * (2*i + 1) / 18)
                screen.blit(num_surf, num_rect)

    if num_solved:
        display_solved(screen, num_solved)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == timer:
                waiting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
    return True


def display_solved(screen, solved):
    font = pygame.font.SysFont(pygame.font.get_default_font(), size=20)
    text = font.render(f'Solved: {solved}', False, 'black')
    text_rect = text.get_rect()
    text_rect.bottomleft = (15, HEIGHT - 7)
    screen.blit(text, text_rect)
    pygame.display.flip()

