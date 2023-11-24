import pygame as pg
from settings import *
import server_interface
import socket


class Game:
    valid_states = [
        'in_main_menu',
        'in_room'
    ]

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_RESOLUTION)
        self.clock = pg.time.Clock()

        self.room = None
        self.players = None
        self.chat = None
        self.state = 'in_main_menu'

        self.server_interface = server_interface.ServerInterface()

        self.text_field = TextField(50, 20, self)

        self.events = pg.event.get()

    def processMainMenu(self):
        self.screen.fill([0, 128, 0])

        for event in self.events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    print('Участок кода для отправки запроса подключения на сервер')

                    self.server_interface.connectToServer(self.text_field.text)

        self.text_field.process([
            self.screen.get_size()[0] / 2 -
            self.text_field.surf.get_size()[0] / 2,
            self.screen.get_size()[1] / 2 - self.text_field.surf.get_size()[1] / 2])

        pg.display.flip()

    def processRoom(self):
        pass

    def loop(self):
        self.events = pg.event.get()

        for e in self.events:
            if e.type == pg.QUIT:
                quit()

        if self.state == 'in_main_menu':
            self.processMainMenu()
        elif self.state == 'in_room':
            self.processRoom()

        self.clock.tick(FPS)


class TextField:
    def __init__(self, font_size, max_char, game):
        self.font_size = font_size
        self.max_char = max_char
        self.game = game
        self.active = False

        self.surf = pg.Surface((max_char * font_size / 2, font_size * 1.5))
        self.surf.fill([255, 255, 255])

        self.font = pg.font.Font(
            './resources/fonts/Comic Sans MS.ttf', self.font_size)

        self.text = 'enter name'

    def process(self, coords):
        self.surf.fill([255, 255, 255])

        img = self.font.render(self.text, True, [0, 0, 0])
        self.surf.blit(img, [self.surf.get_size()[
                       0] / 2 - img.get_size()[0] / 2, 0])

        if self.active:
            pg.draw.rect(self.surf, [0, 0, 0], pg.Rect(
                0, 0, self.surf.get_size()[0], self.surf.get_size()[1]), 5)

        self.game.screen.blit(self.surf, coords)

        for event in self.game.events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if coords[0] < event.pos[0] < coords[0] + self.surf.get_size()[0] and \
                        coords[1] < event.pos[1] < coords[1] + self.surf.get_size()[1]:
                    self.active = True
                else:
                    self.active = False

            if event.type == pg.KEYDOWN and self.active:
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.unicode in ' qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890' and \
                            len(self.text) < self.max_char:
                        self.text += event.unicode


class Button:
    pass


class Switch:
    pass
