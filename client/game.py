import server_interface
import global_scope
import pygame
import pygame_gui
import json
import managers
import os


class Game:
    packets_per_tick = 4

    def __init__(self, uid):
        self.uid = uid
        self.scene = Scene()
        self.messages = []

    def loop_tick(self, events):
        # process packets
        for i in range(Game.packets_per_tick):
            try:
                packet = server_interface.received_packets.pop()

                if packet['type'] == 'scene_data':
                    if 'static' in packet:
                        self.scene.loadStatic(packet['static'])
                    if 'dynamic' in packet:
                        self.scene.loadDynamic(
                            packet['dynamic']['append'])  # TODO временно

                elif packet['type'] == 'chat_data':
                    text = ''
                    self.messages = packet['messages']

            except Exception as e:
                pass

        # process logic
        for event in events:
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == managers.send_message_button:
                    server_interface.GeneratePacket.message(
                        self.uid, managers.send_message_field.text)
                    managers.send_message_field.set_text('')

        if self.scene.dynamic:
            for d in self.scene.dynamic:
                d['position'][0] += d['vector'][0] / \
                    global_scope.FPS * global_scope.GRID_SIZE
                d['position'][1] += d['vector'][1] / \
                    global_scope.FPS * global_scope.GRID_SIZE

        # send packets
        pressed = []
        released = []

        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key in global_scope.KEYBOARD_LAYOUT:
                    pressed.append(global_scope.KEYBOARD_LAYOUT[e.key])

            if e.type == pygame.KEYUP:
                if e.key in global_scope.KEYBOARD_LAYOUT:
                    released.append(global_scope.KEYBOARD_LAYOUT[e.key])

        if pressed or released:
            server_interface.GeneratePacket.input(self.uid, pressed, released)

        # draw
        global_scope.WINDOW_SURFACE.fill((0, 0, 0))

        if self.scene.background:
            global_scope.WINDOW_SURFACE.blit(
                self.scene.background, (0, 0))

        centre = [0, 0]

        if self.scene.dynamic:
            for d in self.scene.dynamic:
                if d['type'] == 'player':
                    if d['uid'] == self.uid:
                        centre[0] = d['position'][0] * global_scope.GRID_SIZE - \
                            global_scope.SCREEN_RESOLUTION[0] / 2
                        centre[1] = d['position'][1] * global_scope.GRID_SIZE - \
                            global_scope.SCREEN_RESOLUTION[1] / 2

        if self.scene.static:
            for y in range(len(self.scene.static)):
                for x in range(len(self.scene.static[0])):
                    if self.scene.static[y][x] != '.':
                        global_scope.WINDOW_SURFACE.blit(
                            global_scope.SPRITES[global_scope.SYMBOLS[self.scene.static[y][x]]], (x*global_scope.GRID_SIZE - centre[0], y*global_scope.GRID_SIZE - centre[1]))

        if self.scene.dynamic:
            for d in self.scene.dynamic:
                if d['type'] == 'player':
                    if d['facing'] == 'right':
                        global_scope.WINDOW_SURFACE.blit(
                            global_scope.SPRITES[d['type']], (d['position'][0]*global_scope.GRID_SIZE - centre[0], d['position'][1]*global_scope.GRID_SIZE - centre[1]))
                    else:
                        global_scope.WINDOW_SURFACE.blit(
                            pygame.transform.flip(global_scope.SPRITES[d['type']], True, False), (d['position'][0]*global_scope.GRID_SIZE - centre[0], d['position'][1]*global_scope.GRID_SIZE - centre[1]))
                else:
                    global_scope.WINDOW_SURFACE.blit(
                        global_scope.SPRITES[d['type']], (d['position'][0]*global_scope.GRID_SIZE, d['position'][1]*global_scope.GRID_SIZE))

        for i, message in enumerate(self.messages):
            global_scope.WINDOW_SURFACE.blit(
                global_scope.DEFAULT_FONT.render(f"{message['author']}: {message['text']}", 0, [255, 255, 255]), [10, 10 + i * global_scope.DEFAULT_FONT.get_height()])


class Scene:
    def __init__(self):
        self.static = None
        self.dynamic = None
        self.background = None

    def loadStatic(self, map_name):
        with open(os.path.join(global_scope.MAPS_PATH, map_name + '.json')) as file:
            j = json.load(file)
            self.static = j['static']
            self.background = global_scope.SPRITES[j['background']]

    def loadDynamic(self, dynamic):
        self.dynamic = dynamic
