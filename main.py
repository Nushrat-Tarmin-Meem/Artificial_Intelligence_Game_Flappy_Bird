import pygame, sys
from button import Button
from level1 import *
from level2 import *
from level3 import *

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")
BG = pygame.image.load("images/main_background.jpg")

def get_font(size):
    return pygame.font.Font("images/font.ttf", size)

def play():
    while True:
        while True:
            SCREEN.blit(BG, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            MENU_TEXT = get_font(80).render("FLAPPY LEVELS", True, "#6a0dad")
            MENU_RECT = MENU_TEXT.get_rect(center=(600, 80))
            LEVEL1_BUTTON = Button(image=pygame.image.load("images/options_rect.png"), pos=(600, 200), 
                                text_input="LOW", font=get_font(75), base_color="#c4a1e9", hovering_color="White")
            LEVEL2_BUTTON = Button(image=pygame.image.load("images/options_rect.png"), pos=(600, 320), 
                                text_input="MEDIUM", font=get_font(75), base_color="#c4a1e9", hovering_color="White")
            LEVEL3_BUTTON = Button(image=pygame.image.load("images/options_rect.png"), pos=(600, 440), 
                                text_input="HIGH", font=get_font(75), base_color="#c4a1e9", hovering_color="White")
            BACK_BUTTON = Button(image=pygame.image.load("images/quit_rect.png"), pos=(600, 560), 
                                text_input="BACK", font=get_font(75), base_color="#c4a1e9", hovering_color="White")
            SCREEN.blit(MENU_TEXT, MENU_RECT)

            for button in [LEVEL1_BUTTON, LEVEL2_BUTTON, LEVEL3_BUTTON, BACK_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if LEVEL1_BUTTON.checkForInput(MENU_MOUSE_POS):
                        level1()
                    if LEVEL2_BUTTON.checkForInput(MENU_MOUSE_POS):
                        level2()
                    if LEVEL3_BUTTON.checkForInput(MENU_MOUSE_POS):
                        level3()                   
                    if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        main_menu()
                        
            pygame.display.update()
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))
        OPTIONS_TEXT1 = get_font(45).render("Owner: Meem & Anisa", True, "White")
        OPTIONS_RECT1 = OPTIONS_TEXT1.get_rect(center=(640, 360))
        SCREEN.blit(OPTIONS_TEXT1, OPTIONS_RECT1)
        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="GO BACK", font=get_font(75), base_color="Grey", hovering_color="Green")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("FLAPPY BIRD", True, "#d8b9e8")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        PLAY_BUTTON = Button(image=pygame.image.load("images/play_rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#c4a1e9", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("images/options_rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#c4a1e9", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("images/quit_rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#c4a1e9", hovering_color="White")
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                    
        pygame.display.update()

main_menu()