from global_scope import *
import pygame
import pygame_gui


main_menu_manager = pygame_gui.UIManager(SCREEN_RESOLUTION)
connect_manager = pygame_gui.UIManager(SCREEN_RESOLUTION)
connection_status_manager = pygame_gui.UIManager(SCREEN_RESOLUTION)


start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 200), (300, 50)),
                                            text='Start Game',
                                            manager=main_menu_manager)

settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 275), (300, 50)),
                                               text='Settings',
                                               manager=main_menu_manager)

exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 345), (300, 50)),
                                           text='Exit',
                                           manager=main_menu_manager)


start_text_field = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((250, 200), (300, 50)),
                                                       manager=connect_manager)

connect_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 275), (300, 50)),
                                              text='Connect',
                                              manager=connect_manager)


status_text_field = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((250, 200), (300, 50)),
                                                manager=connection_status_manager,
                                                text='Waiting for response from server...')

cancel_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 275), (300, 50)),
                                             text='Cancel',
                                             manager=connection_status_manager)
