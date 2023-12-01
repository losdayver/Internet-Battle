import server_interface
import global_scope
import pygame


class Game:
    packets_per_tick = 4

    def __init__(self, uid):
        self.uid = uid

    def loop_tick(self):
        # process packets and logic
        for i in range(Game.packets_per_tick):
            try:
                packet = server_interface.pop()

                if packet['type'] == 'room_data':
                    packet['static']['file_name']
            except:
                pass

        # send packets

        # draw
        global_scope.WINDOW_SURFACE.fill((0, 0, 0))


class Dynamic:
    pass
