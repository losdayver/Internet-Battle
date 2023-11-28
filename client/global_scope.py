import pygame
from pygame import locals as l

# VARIABLES
SCREEN_RESOLUTION = (800, 600)
FPS = 30
KEYBOARD_LAYOUT = {
    'jump': l.K_UP,
    'left': l.K_LEFT,
    'right': l.K_RIGHT,
    'duck': l.K_DOWN,
    'fire': l.K_LSHIFT
}

SERVER_ADDRESS = ('127.0.0.1', 5888)
SERVER_DEBUG = True

# GLOBAL CODE
pygame.display.set_caption('Internet Battle! Prototype 1')
WINDOW_SURFACE = pygame.display.set_mode(SCREEN_RESOLUTION)
CLOCK = pygame.time.Clock()
pygame.init()
IS_RUNNING = True
