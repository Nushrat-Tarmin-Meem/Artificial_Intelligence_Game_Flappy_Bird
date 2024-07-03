import pygame, sys
from button import Button
from level1 import *
from level2 import *



pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")
BG = pygame.image.load("images/main_background.jpg")
bg2 = pygame.image.load("images/options.png")




class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

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
                        import level3              
                    if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        main_menu()
                        
            pygame.display.update()
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(bg2, (0, 0))
        
        # Title
        OPTIONS_TITLE = get_font(55).render("Game Rules", True, "Red")
        OPTIONS_TITLE_RECT = OPTIONS_TITLE.get_rect(center=(640, 100))
        SCREEN.blit(OPTIONS_TITLE, OPTIONS_TITLE_RECT)
        
        # Level 1 Rules
        OPTIONS_TEXT1 = get_font(30).render("Level 1: Flappy Bird Collecting Coins", True, "Blue")
        OPTIONS_RECT1 = OPTIONS_TEXT1.get_rect(center=(640, 160))
        SCREEN.blit(OPTIONS_TEXT1, OPTIONS_RECT1)
        
        OPTIONS_TEXT1_1 = get_font(20).render("Objective: Collect all coins while avoiding obstacles.", True, "White")
        OPTIONS_RECT1_1 = OPTIONS_TEXT1_1.get_rect(center=(640, 190))
        SCREEN.blit(OPTIONS_TEXT1_1, OPTIONS_RECT1_1)
        
        OPTIONS_TEXT1_2 = get_font(20).render("A* Pathfinding guides the bird to the nearest coin.", True, "White")
        OPTIONS_RECT1_2 = OPTIONS_TEXT1_2.get_rect(center=(640, 220))
        SCREEN.blit(OPTIONS_TEXT1_2, OPTIONS_RECT1_2)
        
        OPTIONS_TEXT1_3 = get_font(20).render("Win: Collect all coins.", True, "White")
        OPTIONS_RECT1_3 = OPTIONS_TEXT1_3.get_rect(center=(640, 250))
        SCREEN.blit(OPTIONS_TEXT1_3, OPTIONS_RECT1_3)
        
        OPTIONS_TEXT1_4 = get_font(20).render("Lose: Hit the ground.", True, "White")
        OPTIONS_RECT1_4 = OPTIONS_TEXT1_4.get_rect(center=(640, 280))
        SCREEN.blit(OPTIONS_TEXT1_4, OPTIONS_RECT1_4)

        # Level 2 Rules
        OPTIONS_TEXT2 = get_font(30).render("Level 2: Flappy Bird Collecting Leafs", True, "Blue")
        OPTIONS_RECT2 = OPTIONS_TEXT2.get_rect(center=(640, 330))
        SCREEN.blit(OPTIONS_TEXT2, OPTIONS_RECT2)
        
        OPTIONS_TEXT2_1 = get_font(20).render("Objective: Collect all leaves while avoiding pipes.", True, "White")
        OPTIONS_RECT2_1 = OPTIONS_TEXT2_1.get_rect(center=(640, 360))
        SCREEN.blit(OPTIONS_TEXT2_1, OPTIONS_RECT2_1)
        
        OPTIONS_TEXT2_2 = get_font(20).render("Alpha-Beta Pruning guides the bird to the nearest leaf.", True, "White")
        OPTIONS_RECT2_2 = OPTIONS_TEXT2_2.get_rect(center=(640, 390))
        SCREEN.blit(OPTIONS_TEXT2_2, OPTIONS_RECT2_2)
        
        OPTIONS_TEXT2_3 = get_font(20).render("Win: Collect all leaves.", True, "White")
        OPTIONS_RECT2_3 = OPTIONS_TEXT2_3.get_rect(center=(640, 420))
        SCREEN.blit(OPTIONS_TEXT2_3, OPTIONS_RECT2_3)
        
        OPTIONS_TEXT2_4 = get_font(20).render("Lose: Hit the ground or a pipe.", True, "White")
        OPTIONS_RECT2_4 = OPTIONS_TEXT2_4.get_rect(center=(640, 450))
        SCREEN.blit(OPTIONS_TEXT2_4, OPTIONS_RECT2_4)
        
        # Level 3 Rules
        OPTIONS_TEXT3 = get_font(30).render("Level 3: Flappy Bird", True, "Blue")
        OPTIONS_RECT3 = OPTIONS_TEXT3.get_rect(center=(640, 500))
        SCREEN.blit(OPTIONS_TEXT3, OPTIONS_RECT3)
        
        OPTIONS_TEXT3_1 = get_font(20).render("Objective: Navigate through pipes and collect coins.", True, "White")
        OPTIONS_RECT3_1 = OPTIONS_TEXT3_1.get_rect(center=(640, 530))
        SCREEN.blit(OPTIONS_TEXT3_1, OPTIONS_RECT3_1)
        
        OPTIONS_TEXT3_2 = get_font(15).render("Genetic Algorithm executes space autoplay mode purchased with 5 coins.", True, "White")
        OPTIONS_RECT3_2 = OPTIONS_TEXT3_2.get_rect(center=(640, 560))
        SCREEN.blit(OPTIONS_TEXT3_2, OPTIONS_RECT3_2)
        
        OPTIONS_TEXT3_3 = get_font(20).render("Win: Survive for a certain time and collect coins.", True, "White")
        OPTIONS_RECT3_3 = OPTIONS_TEXT3_3.get_rect(center=(640, 590))
        SCREEN.blit(OPTIONS_TEXT3_3, OPTIONS_RECT3_3)
        
        OPTIONS_TEXT3_4 = get_font(20).render("Lose: Hit the ground or a pipe.", True, "White")
        OPTIONS_RECT3_4 = OPTIONS_TEXT3_4.get_rect(center=(640, 620))
        SCREEN.blit(OPTIONS_TEXT3_4, OPTIONS_RECT3_4)
        
        OPTIONS_BACK = Button(image=None, pos=(640, 670), 
                            text_input="GO BACK", font=get_font(50), base_color="Grey", hovering_color="Green")
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