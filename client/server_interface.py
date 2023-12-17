import socket
import select
import threading
import global_scope
import json

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_sock.setblocking(False)
client_sock.settimeout(0.01)

received_packets = []

packets_to_send = []


def loop():
    global packets_to_send, received_packets

    while global_scope.IS_RUNNING:
        try:
            data, server_address = client_sock.recvfrom(4096)

            # Here packets are decoded, tested for errors and a put into received_packets

            packet = json.loads(data)

            received_packets.append(packet)
        except:
            pass

        # Here all packets from packets_to_send are sent to server

        while packets_to_send:
            packet = packets_to_send.pop()
            packet_str = json.dumps(packet, separators=(',', ':'))
            client_sock.sendto(packet_str.encode('utf-8'),
                               global_scope.SERVER_ADDRESS)


loop_thread = threading.Thread(target=loop).start()

# This class contains static functions that generate packets and put them inside packets_to_send


class GeneratePacket:
    @staticmethod
    def connect(name):
        packet = {
            'type': 'connection',
            'action': 'connect',
            'name': name
        }

        packets_to_send.append(packet)

    @staticmethod
    def disconnect(uid):
        packet = {
            'uid': uid,
            'type': 'connection',
            'action': 'disconnect'
        }

        packets_to_send.append(packet)

    @staticmethod
    def input(uid, pressed_list, released_list):
        packet = {
            'uid': uid,
            'type': 'input',
            'pressed': pressed_list,
            'released': released_list
        }

        print(packet)

        packets_to_send.append(packet)

    @staticmethod
    def message(uid, text):
        packet = {
            'uid': uid,
            'type': 'message',
            'text': text
        }

        packets_to_send.append(packet)
