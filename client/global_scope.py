import pygame
from pygame import locals as l

# VARIABLES
SCREEN_RESOLUTION = (800, 600)
FPS = 30
KEYBOARD_LAYOUT = {
    l.K_UP: 'jump',
    l.K_LEFT: 'left',
    l.K_RIGHT: 'right',
    l.K_DOWN: 'duck',
    l.K_LSHIFT: 'fire'
}

SERVER_ADDRESS = ('127.0.0.1', 5888)
SERVER_DEBUG = True
CURRENT_MANAGER = None

GRID_SIZE = 32
RESOURCES_PATH = './resources/'
STEEL1_SPRITE = pygame.image.load(
    RESOURCES_PATH + 'sprites/export/' + 'steel1.png')
BOX1_SPRITE = pygame.image.load(
    RESOURCES_PATH + 'sprites/export/' + 'box1.png')

# GLOBAL CODE
pygame.display.set_caption('Internet Battle! Prototype 1')
WINDOW_SURFACE = pygame.display.set_mode(SCREEN_RESOLUTION)
CLOCK = pygame.time.Clock()
pygame.init()
IS_RUNNING = True
GAME = None
