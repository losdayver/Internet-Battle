import global_scope
import pygame
import pygame_gui


main_menu_manager = pygame_gui.UIManager(global_scope.SCREEN_RESOLUTION)
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 275), (300, 50)),
                                            text='Start Game',
                                            manager=main_menu_manager)
exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 345), (300, 50)),
                                           text='Exit',
                                           manager=main_menu_manager)


connect_manager = pygame_gui.UIManager(global_scope.SCREEN_RESOLUTION)
start_text_field = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((250, 200), (300, 50)),
                                                       manager=connect_manager)
start_text_field.set_text_length_limit(20)
connect_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 275), (300, 50)),
                                              text='Connect',
                                              manager=connect_manager)


connection_status_manager = pygame_gui.UIManager(
    global_scope.SCREEN_RESOLUTION)
status_text_field = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((250, 200), (300, 50)),
                                                manager=connection_status_manager,
                                                text='Waiting for response from server...')
cancel_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 275), (300, 50)),
                                             text='Cancel',
                                             manager=connection_status_manager)


game_manager = pygame_gui.UIManager(global_scope.SCREEN_RESOLUTION)
send_message_field = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 550), (150, 40)),
                                                         manager=game_manager)
send_message_field.set_text_length_limit(20)
send_message_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((160, 550), (80, 40)),
                                                   text='Send',
                                                   manager=game_manager)
chat_messages_field = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 0), (200, 600)),
                                                  manager=game_manager,
                                                  text='')

# settings_manager = pygame_gui.UIManager(global_scope.SCREEN_RESOLUTION)
# start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 200), (300, 50)),
#                                             text='Start Game',
#                                             manager=main_menu_manager)
# settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 275), (300, 50)),
#                                                text='Settings',
#                                                manager=main_menu_manager)
# exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 345), (300, 50)),
#                                            text='Exit',
#                                            manager=main_menu_manager)
