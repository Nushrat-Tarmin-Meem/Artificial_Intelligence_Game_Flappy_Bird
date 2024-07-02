import pygame, sys
SCREEN = pygame.display.set_mode((1280, 720))
#pygame.display.set_caption("Level3")
BG3 = pygame.image.load("images/level3_background.jpg")
def level3():
    while True:
        SCREEN.blit(BG3, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()