"""This module contains constant values"""
import os.path

import pygame

# Dimensions for the game window
WIN_WIDTH = 500
WIN_HEIGHT = 800

# Fonts for the messages print on the window
pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 40)

# Color codes to be used
WHITE = (255, 255, 255)

# Loaded images with pygame
BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
