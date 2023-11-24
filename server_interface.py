from settings import *
import socket
import json
import threading
import select


class ServerInterface:
    def __init__(self):
        self.socket = self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM)

        self.socket.setblocking(False)
        self.messages = []

        self.thread = threading.Thread(
            target=self.recieveMessages)

        self.thread.start()

    def recieveMessages(self):
        inputs = [self.socket]
        while True:
            readable, writeable, exceptional = select.select(
                inputs, [], inputs, 0.01)

            for sock in readable:
                print('got something')
                msg, server_address = sock.recvfrom(1024)
                if server_address == SERVER_ADDRESS:
                    print(msg)
                    self.socket.sendto(
                        'no, bless you!'.encode('utf-8'), SERVER_ADDRESS)

    def connectToServer(self, name):
        self.socket.sendto(name.encode('utf-8'), SERVER_ADDRESS)

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
