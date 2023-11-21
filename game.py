import pygame as pg
from settings import *
import server_interface


class Game:
    valid_states = [
        'in_main_menu',
        'in_room'
    ]

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_RESOLUTION)
        self.fps = 30
        self.clock = pg.time.Clock()

        self.room = None
        self.players = None
        self.chat = None
        self.state = 'in_main_menu'

        self.server_interface = server_interface.ServerInterface(
            meta_data_name='test')

    def loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()

        if self.state == 'in_main_menu':
            self.processMainMenu()
        elif self.state == 'in_room':
            self.processRoom()

        self.clock.tick(self.fps)

    def processMainMenu(self):
        self.screen.fill([0, 128, 0])
        pg.display.flip()

    def processRoom(self):
        pass
