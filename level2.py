import pygame
import random
import os
import math
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird Collecting Leafs')

# Load images
BG1 = pygame.image.load("images/level2_background.jpg")
BG_WIN = pygame.image.load("images/winning_image.jpg")
BG_LOSE = pygame.image.load("images/losing_image.jpg")
bird_images = [pygame.image.load(os.path.join('images/bird1.png')),
               pygame.image.load(os.path.join('images/bird2.png')),
               pygame.image.load(os.path.join('images/bird3.png'))]
coin_image = pygame.image.load(os.path.join('images/leaf.png'))
arrow_image = pygame.image.load(os.path.join('images/arrow.png'))
pipe_image = pygame.image.load(os.path.join('images/pipe.png'))  # Load pipe image

#loading sounds
fall_sound = pygame.mixer.Sound('.\\sounds\\game-over-arcade.wav')
jump_sound =pygame.mixer.Sound('.\\sounds\\jump.wav') 
tada_sound =pygame.mixer.Sound('.\\sounds\\tada.wav')
start_sound =pygame.mixer.Sound('.\\sounds\\start.wav')
leaf_sound = pygame.mixer.Sound('.\\sounds\\leaf.wav')

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
golden = (255, 215, 0) 
green = (0,255,0) # Golden color

# Alpha-Beta Pruning Algorithm
def alpha_beta_pruning(coins, bird_position, depth, alpha, beta, maximizing_player):
    if depth == 0 or not coins:
        return bird_position, 0  # Return bird position and zero score as heuristic

    if maximizing_player:
        max_eval = -math.inf
        best_move = None
        for coin in coins:
            new_positions = [pos for pos in coins if pos != coin]
            eval, _ = alpha_beta_pruning(new_positions, coin, depth - 1, alpha, beta, False)
            if eval[1] > max_eval:
                max_eval = eval[1]
                best_move = coin
            alpha = max(alpha, eval[1])
            if beta <= alpha:
                break
        return best_move, max_eval
    else:
        min_eval = math.inf
        best_move = None
        for coin in coins:
            new_positions = [pos for pos in coins if pos != coin]
            eval, _ = alpha_beta_pruning(new_positions, coin, depth - 1, alpha, beta, True)
            if eval[1] < min_eval:
                min_eval = eval[1]
                best_move = coin
            beta = min(beta, eval[1])
            if beta <= alpha:
                break
        return best_move, min_eval

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = bird_images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (100, screen_height // 2)
        self.index = 0
        self.velocity = 0
        self.gravity = 1

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity

        # Animate bird
        self.index += 0.1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[int(self.index)]

        # Boundaries
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def flap(self):
        self.velocity = -10

    def move_towards(self, target):
        dx, dy = target[0] - self.rect.centerx, target[1] - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist

        # Move bird
        self.rect.centerx += dx * 3  # Adjust speed as needed
        self.rect.centery += dy * 3

        return dx, dy, dist  # Return the direction and distance

# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = coin_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.collected = False  # Track if the coin has been collected

    def update(self):
        pass

# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pipe_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.x -= 5  # Adjust speed of pipes moving from right to left
        if self.rect.right < 0:
            self.kill()  # Remove pipe when it goes off screen

# Rotate the arrow image
def rotate_arrow(image, angle):
    return pygame.transform.rotate(image, angle)

# Calculate the angle to the target
def calculate_angle(dx, dy):
    return math.degrees(math.atan2(-dy, dx))  # Negative dy because pygame's y-axis is inverted

# Main loop
def level2():
    
    bird = Bird()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(bird)
    fall_played = False
    tada_played = False
    start_played = False
    


    coins = pygame.sprite.Group()
    for _ in range(15):  # Increased to 15 coins
        coin = Coin(random.randint(100, screen_width - 100), random.randint(100, screen_height - 100))
        coins.add(coin)
        all_sprites.add(coin)

    pipes = pygame.sprite.Group()  # Group for pipes
    pipe_frequency = 100  # Frequency to spawn pipes
    pipe_counter = 0

    clock = pygame.time.Clock()
    score = 0

    running = True
    while running:
        if(start_played == False):
            start_sound.play()
            start_played= True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()
                    jump_sound.play()

        # Update
        all_sprites.update()
        pipes.update()

        # Spawn pipes
        pipe_counter += 1
        if pipe_counter == pipe_frequency:
            pipe_height = random.randint(100, screen_height - 300)
            top_pipe = Pipe(screen_width + 50, pipe_height - pipe_image.get_height() // 2)
            bottom_pipe = Pipe(screen_width + 50, pipe_height + pipe_image.get_height() // 2 + 200)
            pipes.add(top_pipe, bottom_pipe)
            all_sprites.add(top_pipe, bottom_pipe)
            pipe_counter = 0

        # Check if bird touches the ground or pipes
        if bird.rect.bottom >= screen_height or pygame.sprite.spritecollideany(bird, pipes):
            if(fall_played == False):
                fall_sound.play()
                fall_played = True
            screen.blit(BG_LOSE, (0, 0))
            font = pygame.font.SysFont(None, 70)
            text = font.render('Alpha-Beta LEVEL FAILED', True, red)
            text_rect = text.get_rect(center=(screen_width // 3, screen_height // 3))
            screen.blit(text, text_rect)
            text2 = font.render('RESTARTING LEVEL 2 SOON', True, golden)
            text_rect2 = text.get_rect(center=(screen_width // 3.5, screen_height // 2))
            screen.blit(text2, text_rect2)
            pygame.display.flip()
            pygame.time.wait(5000)
            level2()
            continue

        # Pathfinding using Alpha-Beta Pruning to nearest coin
        nearest_coin_distance = None
        dx, dy, dist = None, None, None
        if coins:
            coins_list = [coin for coin in coins if not coin.collected]
            if coins_list:
                coins_positions = [coin.rect.center for coin in coins_list]
                nearest_coin, _ = alpha_beta_pruning(coins_positions, bird.rect.center, 3, -math.inf, math.inf, True)
                if nearest_coin:
                    dx, dy, nearest_coin_distance = bird.move_towards(nearest_coin)

                    # Check collision with coins
                    for coin in coins_list:
                        if pygame.sprite.collide_rect(bird, coin):
                            leaf_sound.play()
                            coin.collected = True
                            score += 1
                            # Remove collected coin from groups
                            coin.kill()
                            all_sprites.remove(coin)

        # Draw
        screen.blit(BG1, (0, 0))
        all_sprites.draw(screen)
        pipes.draw(screen)

        # Display score
        font = pygame.font.SysFont(None, 40)
        text = font.render(f'Score: {score}', True, red)
        screen.blit(text, (10, 10))

        # Display distance to nearest coin and direction
        if nearest_coin_distance is not None:
            distance_text = font.render(f'Distance to nearest coin: {int(nearest_coin_distance)}', True, red)
            screen.blit(distance_text, (10, 50))

            direction_text = font.render(f'Direction: dx={round(dx, 2)}, dy={round(dy, 2)}', True, red)
            screen.blit(direction_text, (10, 90))

            # Display arrow indicating direction
            angle = calculate_angle(dx, dy)
            rotated_arrow = rotate_arrow(arrow_image, angle)
            arrow_rect = rotated_arrow.get_rect(midbottom=bird.rect.midtop)
            screen.blit(rotated_arrow, arrow_rect.topleft)

        # Check if all coins are collected
        if len(coins) == 0:
            if(tada_played== False):
                tada_sound.play()
                tada_played = True
            screen.blit(BG_WIN, (0, 0))  # Display winning image
            font = pygame.font.SysFont(None, 100)
            text = font.render('ALPHA-BETA LEVEL WON', True, green)  # Golden color for victory text
            text_rect = text.get_rect(center=(screen_width // 2.5, screen_height // 3))
            screen.blit(text, text_rect)
            text1 = font.render('LEVEL 3 LOADING...', True, blue)  # Golden color for victory text
            text_rect1 = text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(text1, text_rect1)
            pygame.display.flip()
            pygame.time.wait(5000)
            import level3
            continue

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    level2()
