import pygame
from scrollbar import ScrollBar
import os
import button
from grid import Grid

os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (200, 200)

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
SCROLL_HEIGHT = 2000 
game_font = pygame.font.SysFont(name="Lora", size=50)
game_font2 = pygame.font.SysFont(name="Lora", size=25)

grid = Grid(pygame, game_font)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("HHHHHH")

start_img = pygame.image.load("START_BUTTON.png").convert_alpha()
quit_img = pygame.image.load("QUIT_BUTTON.png").convert_alpha()
back_img = pygame.image.load("BACK_BUTTON.png").convert_alpha()

start_button = button.Button(300, 150, start_img, 1.5)
quit_button = button.Button(300, 300, quit_img, 1.5)
back_button = button.Button(300, 500, back_img, 1.5)

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

        if state == "game" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not grid.win:
            pos = pygame.mouse.get_pos()
            pos = (pos[0], pos[1] + scroll_offset)
            grid.get_mouse_click(pos[0], pos[1])

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.win:
                grid.restart()

    if state == "menu":
        screen.fill((202, 228, 241))
        if start_button.draw(screen):
            state = "game"
        if quit_button.draw(screen):
            run = False

    elif state == "game":
        scroll.fill((0, 0, 0))
        grid.draw_all(pygame, scroll)
        back_button.draw(scroll)
        

        if grid.win:
            won_surface = game_font.render("Tu uzvarēji!", False, (0, 255, 0))
            scroll.blit(won_surface, (956, 650))

            press_space_surf = game_font2.render("Spied space, lai restartētu.", False, (0, 255, 200))
            scroll.blit(press_space_surf, (920, 750))

        scroll_offset = int(scrollbar.scroll_percent * (SCROLL_HEIGHT - SCREEN_HEIGHT))

        screen.blit(scroll, (0, -scroll_offset))

        scrollbar.draw(screen)



    pygame.display.update()

pygame.quit()
