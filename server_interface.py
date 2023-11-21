from settings import *
import socket
import server
import json
from multiprocessing import Process


class ServerInterface:
    def __init__(self, meta_data_name):
        self.meta_data = {'name': meta_data_name}

    def sendConnectionData(self, event_type):
        if SERVER_DEBUG:
            pass
        else:
            pass

    def sendKeys(self, pressed_keys, released_keys):
        if SERVER_DEBUG:
            pass
        else:
            pass

    def sendChatMessage(self):
        if SERVER_DEBUG:
            pass
        else:
            pass

    def recieveDataObject(self):
        if SERVER_DEBUG:
            pass
        else:
            pass
