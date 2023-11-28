import socket
import select
import threading
import global_scope
import json

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_sock.setblocking(False)

received_packets = []

packets_to_send = []

# Metadata is sent with every packet except when first connectiong
meta_data = {}


def loop():
    global packets_to_send, received_packets

    inputs = [client_sock]

    while global_scope.IS_RUNNING:
        readable, _, _ = select.select(
            inputs, [], inputs, 0.01)

        for sock in readable:
            data, server_address = sock.recvfrom(1024)

            # Here packets are decoded, tested for errors and a put into received_packets

            packet = json.loads(data)

            received_packets.append(packet)

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
    def disconnect():
        packet = {
            'metadata': meta_data,
            'type': 'connection',
            'action': 'disconnect'
        }

        packets_to_send.append(packet)

    @staticmethod
    def input(pressed_list, released_list):
        packet = {
            'metadata': meta_data,
            'type': 'input',
            'pressed': pressed_list,
            'released': released_list
        }

        packets_to_send.append(packet)
