import server_interface
import global_scope
import pygame
import pygame_gui
import json
import managers


class Game:
    packets_per_tick = 4

    def __init__(self, uid):
        self.uid = uid
        self.scene = None
        self.messages = []

    def loop_tick(self, events):
        # process packets
        for i in range(Game.packets_per_tick):
            try:
                packet = server_interface.received_packets.pop()

                if packet['type'] == 'scene_data':
                    if packet['static']['method'] == 'file':
                        self.scene = Scene(
                            packet['static']['file'], packet['dynamic'])

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

        if self.scene:
            for d in self.scene.dynamic:
                d['position'][0] += d['vector'][0] / global_scope.FPS
                d['position'][1] += d['vector'][1] / global_scope.FPS

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

        if self.scene:
            global_scope.WINDOW_SURFACE.blit(
                self.scene.image, (0, 0))

            for y in range(len(self.scene.static)):
                for x in range(len(self.scene.static[0])):
                    if self.scene.static[y][x] == '#':
                        global_scope.WINDOW_SURFACE.blit(
                            global_scope.STEEL1_SPRITE, (x*global_scope.GRID_SIZE, y*global_scope.GRID_SIZE))

            for d in self.scene.dynamic:
                if d['type'] == 'box1':
                    global_scope.WINDOW_SURFACE.blit(
                        global_scope.BOX1_SPRITE, (d['position'][0]*global_scope.GRID_SIZE, d['position'][1]*global_scope.GRID_SIZE))

        for i, message in enumerate(self.messages):
            global_scope.WINDOW_SURFACE.blit(
                global_scope.DEFAULT_FONT.render(f"{message['author']}: {message['text']}", 0, [255, 255, 255]), [10, 10 + i * global_scope.DEFAULT_FONT.get_height()])


class Scene:
    def __init__(self, map_file, dynamic):
        with open(f'./resources/maps/{map_file}') as f:
            j = json.load(f)

            self.static = j['static']
            self.image = pygame.image.load(
                global_scope.BACKGROUND1_SPRITE)

        self.dynamic = dynamic
