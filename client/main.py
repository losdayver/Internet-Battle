import global_scope
from managers import *
import pygame_gui
import pygame
import server_interface
import game

# Temp variables for main loop logic
current_manager = main_menu_manager
current_state = 'menu'  # menu/connecting/game

while global_scope.IS_RUNNING:
    WINDOW_SURFACE.fill((0, 100, 0))

    time_delta = CLOCK.tick(global_scope.FPS)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global_scope.IS_RUNNING = False

        # UI elements logic
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if current_manager == main_menu_manager:
                if event.ui_element == start_button:
                    current_manager = connect_manager
                elif event.ui_element == settings_button:
                    settings_button.hide()
                elif event.ui_element == exit_button:
                    global_scope.IS_RUNNING = False

            elif current_manager == connect_manager:
                if event.ui_element == connect_button:
                    current_manager = connection_status_manager
                    server_interface.GeneratePacket.connect(
                        start_text_field.get_text())
                    current_state = 'connecting'

            elif current_manager == connection_status_manager:
                if event.ui_element == cancel_button:
                    current_manager = main_menu_manager
                    current_state = 'menu'

            elif current_manager == game_manager:
                pass

        current_manager.process_events(event)

    # General logic
    if current_state == 'connecting':
        if server_interface.received_packets:
            packet = server_interface.received_packets.pop()
            if packet['type'] == 'connection':
                if packet['action'] == 'accept':
                    global_scope.GAME = game.Game(packet['uid'])
                    current_manager = game_manager
                    current_state = 'game'
                    current_manager = game_manager
                elif packet['action'] == 'reject':
                    status_text_field.set_text(packet['reason'])

    elif current_state == 'game':
        global_scope.GAME.loop_tick()

    current_manager.update(time_delta)

    current_manager.draw_ui(global_scope.WINDOW_SURFACE)

    pygame.display.update()
