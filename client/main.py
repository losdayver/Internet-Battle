from globals import *
from managers import *
import pygame_gui
import pygame

current_manager = main_menu_manager

while is_running:
    WINDOW_SURFACE.fill((0, 0, 0))

    time_delta = CLOCK.tick(FPS)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:

            if current_manager == main_menu_manager:
                if event.ui_element == start_button:
                    current_manager = connect_manager
                elif event.ui_element == exit:
                    is_running = False

            elif current_manager == connect_manager:
                if event.ui_element == connect_button:
                    print('hello')

        current_manager.process_events(event)

    current_manager.update(time_delta)

    current_manager.draw_ui(WINDOW_SURFACE)

    pygame.display.update()
