import server_interface
import global_scope
import pygame
import json


class Game:
    packets_per_tick = 4

    def __init__(self, uid):
        self.uid = uid
        self.scene = None

    def loop_tick(self, events):
        # process packets
        for i in range(Game.packets_per_tick):
            try:
                packet = server_interface.received_packets.pop()

                if packet['type'] == 'scene_data':
                    if packet['static']['method'] == 'file':
                        self.scene = Scene(
                            packet['static']['file'], packet['dynamic'])

            except Exception as e:
                pass

        # process logic
        if self.scene:
            for d in self.scene.dynamic:
                d['position'][0] += d['vector'][0]
                d['position'][1] += d['vector'][1]

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


class Scene:
    def __init__(self, map_file, dynamic):
        with open(f'./resources/maps/{map_file}') as f:
            j = json.load(f)

            self.static = j['static']
            self.image = pygame.image.load(
                global_scope.RESOURCES_PATH + 'sprites/export/' + j['image'])

        self.dynamic = dynamic


class Dynamic:
    def __init__(self):
        pass
