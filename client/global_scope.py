import pygame
from pygame import locals as l
import os

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
RESOURCES_PATH = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), 'resources')
SPRITES_PATH = os.path.join(RESOURCES_PATH, 'sprites', 'export')
MAPS_PATH = os.path.join(RESOURCES_PATH, 'maps')

SPRITES = {
    'starfield':
    pygame.image.load(os.path.join(
        SPRITES_PATH, 'starfield.png')),
    'stone': pygame.image.load(os.path.join(
        SPRITES_PATH, 'stone.png')),
    'box': pygame.image.load(os.path.join(
        SPRITES_PATH, 'box.png')),
    'player': pygame.image.load(os.path.join(
        SPRITES_PATH, 'pistol.png'))
}

# GLOBAL CODE
pygame.display.set_caption('Internet Battle! Prototype 1')
WINDOW_SURFACE = pygame.display.set_mode(SCREEN_RESOLUTION)
pygame.init()
CLOCK = pygame.time.Clock()
DEFAULT_FONT = pygame.font.Font(os.path.join(
    RESOURCES_PATH, "fonts", "Comic Sans MS.ttf"), 15)
IS_RUNNING = True
GAME = None
