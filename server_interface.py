from settings import *
import socket
import json
import threading
import select
import json


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
                msg, server_address = sock.recvfrom(1024)
                if server_address == SERVER_ADDRESS:
                    print(msg)

    def connectToServer(self, name):
        payload = json.dumps({
            'meta_data': {
                'name': name
            },
            'connection_data': {
                'method': 'connect'
            }
        }, separators=(',', ':'))

        self.socket.sendto(payload.encode('utf-8'), SERVER_ADDRESS)

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
