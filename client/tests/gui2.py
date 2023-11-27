import pygame
import pygame_gui

pygame.init()

window_surface = pygame.display.set_mode((800, 600))

clock = pygame.time.Clock()
is_running = True

main_menu_manager = pygame_gui.UIManager((800, 600))

# elements
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 200), (100, 50)),
                                            text='Start Game',
                                            manager=main_menu_manager)

settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                               text='Settings',
                                               manager=main_menu_manager)

exit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 345), (100, 50)),
                                    text='Exit',
                                    manager=main_menu_manager)

connect_manager = pygame_gui.UIManager((800, 600))

start_text_field = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 200), (100, 50)),
                                                       manager=connect_manager)

connect_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                              text='Connect',
                                              manager=connect_manager)

current_manager = main_menu_manager

while is_running:
    window_surface.fill((0, 0, 0))

    time_delta = clock.tick(60)/1000.0

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

    current_manager.draw_ui(window_surface)

    pygame.display.update()
