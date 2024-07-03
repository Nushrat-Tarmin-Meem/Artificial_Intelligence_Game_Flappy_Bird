import components
import pygame

win_height = 1280
win_width = 720
window = pygame.display.set_mode((win_width, win_height))

ground = components.Ground(win_width)
pipes = []