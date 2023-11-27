from globals import *
import pygame
import pygame_gui


main_menu_manager = pygame_gui.UIManager(SCREEN_RESOLUTION)


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
