import global_scope
from managers import *
import pygame_gui
import pygame
import server_interface
import game
import os

print(os.getcwd())

# Temp variables for main loop logic
global_scope.CURRENT_MANAGER = connect_manager

while global_scope.IS_RUNNING:
    WINDOW_SURFACE.fill((0, 100, 0))

    time_delta = CLOCK.tick(global_scope.FPS)/1000.0

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            global_scope.IS_RUNNING = False

        # UI elements logic
        if event.type == pygame_gui.UI_BUTTON_PRESSED:

            if global_scope.CURRENT_MANAGER == main_menu_manager:
                if event.ui_element == start_button:
                    global_scope.CURRENT_MANAGER = connect_manager
                elif event.ui_element == settings_button:
                    settings_button.hide()
                elif event.ui_element == exit_button:
                    global_scope.IS_RUNNING = False

            elif global_scope.CURRENT_MANAGER == connect_manager:
                if event.ui_element == connect_button:
                    global_scope.CURRENT_MANAGER = connection_status_manager
                    server_interface.GeneratePacket.connect(
                        start_text_field.get_text())
                    global_scope.CURRENT_MANAGER = connection_status_manager

            elif global_scope.CURRENT_MANAGER == connection_status_manager:
                if event.ui_element == cancel_button:
                    global_scope.CURRENT_MANAGER = main_menu_manager

        global_scope.CURRENT_MANAGER.process_events(event)

    # General logic
    if global_scope.CURRENT_MANAGER == connection_status_manager:
        if server_interface.received_packets:
            packet = server_interface.received_packets.pop()
            if packet['type'] == 'connection':
                if packet['action'] == 'accept':
                    global_scope.GAME = game.Game(packet['uid'])
                    global_scope.CURRENT_MANAGER = game_manager
                    current_state = 'game'
                elif packet['action'] == 'reject':
                    status_text_field.set_text(packet['reason'])

    elif global_scope.CURRENT_MANAGER == game_manager:
        global_scope.GAME.loop_tick(events)

    global_scope.CURRENT_MANAGER.update(time_delta)

    global_scope.CURRENT_MANAGER.draw_ui(global_scope.WINDOW_SURFACE)

    pygame.display.flip()
