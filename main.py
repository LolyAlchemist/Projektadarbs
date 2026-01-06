import pygame
from scrollbar import ScrollBar
import os
import button
from grid import Grid

os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (100, 25)
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1200
SCROLL_HEIGHT = 1400

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku Bombs")

game_font = pygame.font.SysFont("Arial", 50) 
game_font2 = pygame.font.SysFont("Arial", 25)

grid = Grid(pygame, game_font)

start_img = pygame.image.load("START_BUTTON.png").convert_alpha()
quit_img = pygame.image.load("QUIT_BUTTON.png").convert_alpha()
tuto_img = pygame.image.load("BACK_BUTTON.png").convert_alpha()
back_img = pygame.image.load("BACK_BUTTON.png").convert_alpha()

start_button = button.Button(450, 150, start_img, 1.5)
quit_button = button.Button(450, 300, quit_img, 1.5)
tuto_button = button.Button(450, 450, tuto_img, 1.5)
back_button = button.Button(450, 500, back_img, 1.5)

state = "menu"
run = True

scrollbar = ScrollBar(1150, 0, SCREEN_HEIGHT)
scroll = pygame.Surface((SCREEN_WIDTH, SCROLL_HEIGHT))
scroll_offset = 0

while run:
    for event in pygame.event.get():
        scrollbar.handle_event(event)

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and grid.win:
                grid.restart()

            if state == "game" and not grid.win:
                if event.unicode.isdigit():
                    grid.bomb_answer += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    grid.bomb_answer = grid.bomb_answer[:-1]
                elif event.key == pygame.K_RETURN:
                    solutions = grid.get_bomb_solutions()
                    if grid.bomb_answer.isdigit() and int(grid.bomb_answer) in solutions:
                        grid.bomb_feedback = "Correct!"
                        grid.bomb_feedback_color = (0, 255, 0) # pyright: ignore[reportAttributeAccessIssue]
                        grid.bomb_correct = True
                        for r, c in grid.bombs:
                            if int(grid.bomb_answer) == grid.get_cell(c, r):
                                grid.bomb_cell_correct[(r, c)] = True
                    else:
                        grid.bomb_feedback = "Wrong — try again"
                        grid.bomb_feedback_color = (255, 80, 80) # pyright: ignore[reportAttributeAccessIssue]
                        grid.bomb_correct = False
                        for r, c in grid.bombs:
                            if int(grid.bomb_answer) == grid.get_cell(c, r):
                                grid.bomb_cell_correct[(r, c)] = False
                    grid.bomb_answer = ""


        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            adjusted_mouse_y = mouse_y + scroll_offset
            if state == "game":
                grid.get_mouse_click(mouse_x, adjusted_mouse_y)

    scroll_offset = int(scrollbar.scroll_percent * (SCROLL_HEIGHT - SCREEN_HEIGHT))

    if state == "menu":
        screen.fill((202, 228, 241))
        if start_button.draw(screen):
            state = "game"
        if tuto_button.draw(screen):
            state = "tutorial"
        if quit_button.draw(screen):
            run = False

    elif state == "game":
        scroll.fill((0, 0, 0))
        grid.draw_all(pygame, scroll)
        if grid.win:
            won_surface = game_font.render("Tu uzvarēji!", False, (0, 255, 0))
            scroll.blit(won_surface, (956, 650))
            press_space_surf = game_font2.render(
                "Spied space, lai restartētu.", False, (0, 255, 200)
            )
            scroll.blit(press_space_surf, (920, 750))
        screen.blit(scroll, (0, -scroll_offset))
        scrollbar.draw(screen)

    elif state == "tutorial":
        scroll.fill((255, 255, 255))
        y = 20
        font = pygame.font.SysFont("Arial", 25)
        text = [
            "NOTEIKUMI:",
            "* Spēkā ir parastie sudoku noteikumi.",
            "* Zem sudoku ir teksts, kurš informē — kurā kolonnā un rindā ir bomba.",
            "* Zem bombas lokācijas informācijas jāievada pareizais cipars.",
            "",
            "BOMBAS LOKĀCIJA:",
            "Kolonna: ____",
            "Rinda: ____",
            "",
            "PAREIZAIS CIPARS (BOMBA):",
            "____"
        ]
        for line in text:
            surface = font.render(line, True, (0, 0, 0))
            scroll.blit(surface, (20, y))
            y += 35

        mouse_pos = pygame.mouse.get_pos()
        adjusted_mouse_pos = (mouse_pos[0], mouse_pos[1] + scroll_offset)

        if back_button.draw(scroll, adjusted_mouse_pos):
            state = "menu"

        screen.blit(scroll, (0, -scroll_offset))
        scrollbar.draw(screen)

    pygame.display.flip()

pygame.quit()
