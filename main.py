import pygame
import button

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Menu")


start_img = pygame.image.load("START_BUTTON.png").convert_alpha()
quit_img = pygame.image.load("QUIT_BUTTON.png").convert_alpha()
back_img = pygame.image.load("BACK_BUTTON.png").convert_alpha()



start_button = button.Button(300,150, start_img, 1.5)
quit_button = button.Button(300,300, quit_img, 1.5)
back_button = button.Button(300, 500, back_img, 1.5)

def start_game():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill((255, 255, 255))

        font = pygame.font.Font(None, 60)
        text = font.render("Press ESC to go back", True, (255, 255, 255))
        screen.blit(text, (220, 550))


        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run = False
        elif back_button.draw(screen):
            run = False

        pygame.display.update()

run = True
while run:

    screen.fill((202,228,241))
    if start_button.draw(screen):
        start_game()



    if quit_button.draw(screen):
        run = False
    
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
