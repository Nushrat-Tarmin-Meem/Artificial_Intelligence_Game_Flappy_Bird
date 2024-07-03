import pygame
import numpy as np
from pygame.locals import *
import random
from sys import exit
import config
import components
import population



pygame.init()

clock = pygame.time.Clock()
fps = 60
population = population.Population(2000)


screen_width = 864
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

# defining font
font = pygame.font.SysFont('Bauhaus 93', 60)

# defining colours
red = (255, 0, 0)
blue = (0, 0, 255)

# defining game variables
ground_scroll = 0
scroll_speed = 4
total_score = 0
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
coin_count = 0
inn_boost = False






# loading images
bg = pygame.image.load('.\Images\\back1.jpg')
bg = pygame.transform.scale(bg, (screen_width, screen_height))
bg2 = pygame.image.load('.\\Images\\back2.jpg')
bg2 = pygame.transform.scale(bg2, (screen_width, screen_height))
ground_img = pygame.image.load('.\\Images\\ground.png')
button_img = pygame.image.load('.\\Images\\restart.png')
boost_img = pygame.image.load('.\\Images\\boost.png')

# Fuzzy logic functions
def getMembershipScore(score):
    degree = {}
    if score < 0 or score > 20:
        degree["low"] = 0
        degree["medium"] = 0
        degree["high"] = 0
    elif score <= 10:
        degree["low"] = 1 - (score / 10)
        degree["medium"] = score / 10
        degree["high"] = 0
    elif score <= 15:
        degree["low"] = 0
        degree["medium"] = 1 - ((score - 10) / 5)
        degree["high"] = (score - 10) / 5
    else:
        degree["low"] = 0
        degree["medium"] = 0
        degree["high"] = 1
    return degree

def getMembershipScrollSpeed(score_membership):
    degree = {"slow": 0, "moderate": 0, "fast": 0}
    if score_membership["low"] > 0:
        degree["slow"] = score_membership["low"]
    if score_membership["medium"] > 0:
        degree["moderate"] = score_membership["medium"]
    if score_membership["high"] > 0:
        degree["fast"] = score_membership["high"]
    return degree

def defuzzifyScrollSpeed(speed_membership):
    slow_centroid = 2
    moderate_centroid = 5
    fast_centroid = 9
    weights = speed_membership["slow"] * slow_centroid + speed_membership["moderate"] * moderate_centroid + speed_membership["fast"] * fast_centroid
    total_membership = speed_membership["slow"] + speed_membership["moderate"] + speed_membership["fast"]
    if total_membership == 0:
        return 1  # Default to the lowest speed if no rule is active
    return weights / total_membership

def update_scroll_speed(current_score):
    global inn_boost
    score_membership = getMembershipScore(current_score)
    speed_membership = getMembershipScrollSpeed(score_membership)
    if(inn_boost == True):
        inn_boost = False
        return 4
    return defuzzifyScrollSpeed(speed_membership)

def generate_pipes():
    config.pipes.append(components.Pipes(config.win_width))

def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
def GA(score):
    pipes_spawn_time = 10
    pipes_overcome = 0  # Counter for the number of pipes passed

    while True:
        quit_game()
        screen.fill((0, 0, 0))  # Optional, depending on if you want a black fill before drawing the background
        screen.blit(bg2, (0, 0))
        screen.blit(ground_img, (ground_scroll, 768))

        # Spawn Pipes
        if pipes_spawn_time <= 0:
            generate_pipes()
            pipes_spawn_time = 200
        pipes_spawn_time -= 1

        for p in config.pipes:
            p.draw(config.window)
            p.update()
            if p.off_screen:
                config.pipes.remove(p)
                pipes_overcome += 1  # Increment counter when a pipe goes off-screen

        if pipes_overcome >= 6:
            score+=6
            return score,2  # Exit the GA function after overcoming 3 pipes

        if not population.extinct():
            population.update_live_players()
        else:
            config.pipes.clear()
            population.natural_selection()

        clock.tick(60)
        pygame.display.flip()
    pipes_spawn_time = 10

    while True:
        quit_game()

        config.window.fill((0, 0, 0))

        # Spawn Ground
        config.ground.draw(config.window)

        # Spawn Pipes
        if pipes_spawn_time <= 0:
            generate_pipes()
            pipes_spawn_time = 200
        pipes_spawn_time -= 1

        for p in config.pipes:
            p.draw(config.window)
            p.update()
            if p.off_screen:
                config.pipes.remove(p)

        if not population.extinct():
            population.update_live_players()
        else:
            config.pipes.clear()
            population.natural_selection()

        clock.tick(60)
        pygame.display.flip()








def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    pipe_group.empty()
    coin_group.empty()
    boost_button.hide()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    coin_count = 0
    return score, coin_count


class Bird2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(
                f'.\\Images\\bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if flying == True:
            # gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if game_over == False:
            # jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # handling the animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # rotating the bird
            self.image = pygame.transform.rotate(
                self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)



class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            '.\\Images\\coin.png')
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            '.\\Images\\pipe.png')
        self.rect = self.image.get_rect()
        # position of pipe 1 is from the top, -1 is from the bottom
        if score < 4:
            if position == 1:
                self.image = pygame.transform.flip(self.image, False, True)
                self.rect.bottomleft = [x, y - int(pipe_gap / 1)]
            if position == -1:
                self.rect.topleft = [x, y + int(pipe_gap / 1)]
        elif score >= 4 and score < 10:
            if position == 1:
                self.image = pygame.transform.flip(self.image, False, True)
                self.rect.bottomleft = [x, y - int(pipe_gap / 1.5)]
            if position == -1:
                self.rect.topleft = [x, y + int(pipe_gap / 1.5)]
        else:
            if position == 1:
                self.image = pygame.transform.flip(self.image, False, True)
                self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
            if position == -1:
                self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        # getting mouse position
        pos = pygame.mouse.get_pos()
        # checking if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        # drawing button
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action
    
class Boost_Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.bottomright = (screen_width - 10, screen_height - 10)
        self.visible = True
        


    def draw(self):
        action = False
        # getting mouse position
        pos = pygame.mouse.get_pos()
        # checking if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
                self.visible = False
               
                
        # drawing button
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action    
    
    def hide(self):
        #print("Hide")
        self.visible = False 
        
        
        
        

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

flappy = Bird2(100, int(screen_height / 2))

bird_group.add(flappy)


# creating restart button instance
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)
boost_button = Boost_Button(screen_width // 2 - 50, screen_height // 2 - 100, boost_img)



run = True
while run:

    clock.tick(fps)
    # drawing background
    screen.blit(bg, (0, 0))
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    coin_group.draw(screen)

    # drawing the ground
    screen.blit(ground_img, (ground_scroll, 768))
    

    # checking the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
                and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                total_score+=1
                pass_pipe = False
    draw_text("Score: "+str(total_score), font, red, int(screen_width / 2.5), 20)
    draw_text("Coins: "+str(coin_count), font,blue, int(screen_width / 10), 20)

    # looking for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        boost_button.hide()
        game_over = True

    # checking if bird has hit the ground
    if flappy.rect.bottom >= 768:
        boost_button.hide()
        game_over = True
        flying = False

    coin_collision = pygame.sprite.groupcollide(bird_group, coin_group, False, True)
    if coin_collision:
        coin_count += 1

    if game_over == False and flying == True:
        # Update scroll speed based on score
        scroll_speed = update_scroll_speed(score)
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0 
        pipe_group.update()
        coin_group.update()
        
        # generating new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            if random.randint(0, 1):  # This returns either 0 or 1, where 1 means add a coin
                coin = Coin(screen_width + top_pipe.rect.width, int(screen_height / 2) + pipe_height)
                coin_group.add(coin)
                
            last_pipe = time_now
            
            
        # drawing and scrolling the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
        pipe_group.update()
        coin_group.update()
       

    if game_over == False and score == 5:
        draw_text("WON LEVEL 1", font, blue, int(screen_width / 3), 70)

    if game_over == False and score == 10:
        draw_text("WON LEVEL 2", font, blue, int(screen_width / 3), 70)

    if game_over == False and score == 15:
        draw_text("WON LEVEL 3", font, blue, int(screen_width / 3), 70)
    
   
                
    if (game_over == False and coin_count >= 5):
        if boost_button.draw() == True:
            before = scroll_speed
            total_score,scroll_speed = GA(score)
            coin_count -= 5
            inn_boost = True
    
      
    
    # checking for game over and resetting
    if game_over == True:
        boost_button.hide()
        if button.draw() == True:
            scroll_speed = 0
            game_over = False
            score, coin_count = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            boost_button.hide()
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()