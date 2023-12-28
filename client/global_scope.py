import pygame
from pygame import locals as l
import os

# VARIABLES
SCREEN_RESOLUTION = (800, 600)
FPS = 60
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
    'abstract':
    pygame.image.load(os.path.join(
        SPRITES_PATH, 'abstract.png')),
    'gory_kavkaza':
    pygame.image.load(os.path.join(
        SPRITES_PATH, 'gory_kavkaza.png')),

    'stone': pygame.image.load(os.path.join(
        SPRITES_PATH, 'stone.png')),
    'stone_darker': pygame.image.load(os.path.join(
        SPRITES_PATH, 'stone_darker.png')),
    'reinforced_concrete': pygame.image.load(os.path.join(
        SPRITES_PATH, 'reinforced_concrete.png')),
    'metal': pygame.image.load(os.path.join(
        SPRITES_PATH, 'metal.png')),
    'metal_beam': pygame.image.load(os.path.join(
        SPRITES_PATH, 'metal_beam.png')),
    'leaves': pygame.image.load(os.path.join(
        SPRITES_PATH, 'leaves.png')),
    'grass': pygame.image.load(os.path.join(
        SPRITES_PATH, 'grass.png')),
    'deep_ground': pygame.image.load(os.path.join(
        SPRITES_PATH, 'deep_ground.png')),
    'bricks': pygame.image.load(os.path.join(
        SPRITES_PATH, 'bricks.png')),
    'box': pygame.image.load(os.path.join(
        SPRITES_PATH, 'box.png')),

    'box': pygame.image.load(os.path.join(
        SPRITES_PATH, 'box.png')),
    'player': pygame.image.load(os.path.join(
        SPRITES_PATH, 'mushroom_00.png')),
    'player_dead': pygame.image.load(os.path.join(
        SPRITES_PATH, 'mushroom_dead.png')),

    'player_animation': [
        pygame.image.load(os.path.join(
            SPRITES_PATH, 'mushroom_00.png')),

        pygame.image.load(os.path.join(
            SPRITES_PATH, 'mushroom_01.png')),

        pygame.image.load(os.path.join(
            SPRITES_PATH, 'mushroom_02.png')),

        pygame.image.load(os.path.join(
            SPRITES_PATH, 'mushroom_03.png')),

        pygame.image.load(os.path.join(
            SPRITES_PATH, 'mushroom_04.png')),

        pygame.image.load(os.path.join(
            SPRITES_PATH, 'mushroom_05.png')),

        pygame.image.load(os.path.join(
            SPRITES_PATH, 'mushroom_06.png')),

        pygame.image.load(os.path.join(
            SPRITES_PATH, 'mushroom_07.png')),

        pygame.image.load(os.path.join(
            SPRITES_PATH, 'mushroom_08.png')),

        pygame.image.load(os.path.join(
            SPRITES_PATH, 'mushroom_09.png'))
    ],

    'player_jumping': pygame.image.load(os.path.join(
        SPRITES_PATH, 'mushroom_jumping.png')),
    'shotgun': pygame.image.load(os.path.join(
        SPRITES_PATH, 'shotgun.png')),
    's_bullet': pygame.image.load(os.path.join(
        SPRITES_PATH, 'shotgun_bullet.png')),
    'p_bullet': pygame.image.load(os.path.join(
        SPRITES_PATH, 'pistol_bullet.png'))
}

SYMBOLS = {
    '=': 'stone',
    '#': 'stone_darker',
    'E': 'reinforced_concrete',
    '$': 'metal',
    '%': 'metal_beam',
    '*': 'leaves',
    '*': 'grass',
    '&': 'deep_ground',
    '+': 'bricks',
    'x': 'box'
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
