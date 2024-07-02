import pygame
import heapq
import random
import os
import math
import sys
from level2 import *
# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird Collecting Coins')

# Load images
BG1 = pygame.image.load("images/level1_background.jpg")
BG_WIN = pygame.image.load("images/winning_image.jpg")
BG_LOSE = pygame.image.load("images/losing_image.jpg")
bird_images = [pygame.image.load(os.path.join('images/bird1.png')),
               pygame.image.load(os.path.join('images/bird2.png')),
               pygame.image.load(os.path.join('images/bird3.png'))]
coin_image = pygame.image.load(os.path.join('images/coin.png'))
arrow_image = pygame.image.load(os.path.join('images/arrow.png'))

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0,0,255)
golden = (255, 215, 0)
green = (0,255,0)  # Golden color

# A* Algorithm
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal, obstacles):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    came_from[start] = None
    visited_nodes = []

    while open_list:
        _, current = heapq.heappop(open_list)
        visited_nodes.append(current)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path, visited_nodes

        for neighbor in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + neighbor[0], current[1] + neighbor[1])
            if neighbor[1] < 0 or neighbor[1] >= screen_height or neighbor[0] < 0 or neighbor[0] >= screen_width:
                continue
            if neighbor in obstacles:
                continue

            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None, visited_nodes

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

# Rotate the arrow image
def rotate_arrow(image, angle):
    return pygame.transform.rotate(image, angle)

# Calculate the angle to the target
def calculate_angle(dx, dy):
    return math.degrees(math.atan2(-dy, dx))  # Negative dy because pygame's y-axis is inverted

# Main loop
def level1():
    bird = Bird()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(bird)

    coins = pygame.sprite.Group()
    for _ in range(15):  # Increased to 15 coins
        coin = Coin(random.randint(100, screen_width - 100), random.randint(100, screen_height - 100))
        coins.add(coin)
        all_sprites.add(coin)

    clock = pygame.time.Clock()
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        # Update
        all_sprites.update()

        # Check if bird touches the ground
        if bird.rect.bottom >= screen_height:
            screen.blit(BG_LOSE, (0, 0))
            font = pygame.font.SysFont(None, 70)
            text = font.render('A* LEVEL FAILED', True, red)
            text_rect = text.get_rect(center=(screen_width // 3, screen_height // 3))
            screen.blit(text, text_rect)
            text2 = font.render('RESTARTING LEVEL 1 SOON', True, golden)
            text_rect2 = text.get_rect(center=(screen_width // 4.5, screen_height // 2))
            screen.blit(text2, text_rect2)
            pygame.display.flip()
            pygame.time.wait(5000)
            level1()
            continue

        # Pathfinding using A* to nearest coin
        nearest_coin_distance = None
        dx, dy, dist = None, None, None
        if coins:
            nearest_coin = min(coins, key=lambda coin: heuristic(bird.rect.center, coin.rect.center))
            dx, dy, nearest_coin_distance = bird.move_towards(nearest_coin.rect.center)

            # Check collision with coins
            if pygame.sprite.spritecollideany(bird, coins):
                score += 1
                nearest_coin.kill()
                coins.remove(nearest_coin)
                all_sprites.remove(nearest_coin)

        # Draw
        screen.blit(BG1, (0, 0))
        all_sprites.draw(screen)

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
        if not coins:
            screen.blit(BG_WIN, (0, 0))  # Display winning image
            font = pygame.font.SysFont(None, 100)
            text = font.render('A* LEVEL WON', True, green)  # Golden color for victory text
            text_rect = text.get_rect(center=(screen_width // 2.5, screen_height // 3))
            screen.blit(text, text_rect)
            text1 = font.render('LEVEL 2 LOADING...', True, blue)  # Golden color for victory text
            text_rect1 = text.get_rect(center=(screen_width // 4, screen_height // 2))
            screen.blit(text1, text_rect1)
            pygame.display.flip()
            pygame.time.wait(5000)
            level2()
            continue

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    level1()
