import socket
import select
import threading
from globals import *

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_sock.setblocking(False)

received_packets = []

packets_to_send = []


def loop():
    inputs = [client_sock]

    while True:
        readable, _, _ = select.select(
            inputs, [], inputs, 0.01)

        for sock in readable:
            msg, server_address = sock.recvfrom(1024)

            # Here packets are decoded, tested for errors and a put into received_packets

        # Here all packets from packets_to_send are sent to server


loop_thread = threading.Thread(target=loop)

# This class contains static functions that generate packets and put them inside packets_to_send


class GeneratePacket:
    def connect():
        pass

    def disconnect():
        pass

    def input():
        pass
