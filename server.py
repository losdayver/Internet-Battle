import socket
import select
import json

if __name__ != '__main__':
    quit()


class Packet:
    def __init__(self, payload, address):
        self.payload = payload
        self.address = address


class Server:
    def __init__(self, address):
        self.address = address
        self.serv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serv_sock.bind(self.address)
        self.serv_sock.setblocking(False)

        self.recv_packets = []
        self.ready_packets = []

    def loop(self):
        while True:
            self.sendRecievePackets()
            self.processPackets()

    def processPackets(self):
        packets_to_delete = []

        for packet in self.recv_packets:
            for obj in packet.payload:
                if obj == 'connection_data':
                    print(f'connection request from {packet.address}')

                    payload = json.dumps({'connection_data': {'status': 'accept'}}).replace(
                        ' ', '').replace('\n', '')

                    self.ready_packets.append(
                        Packet(payload.encode('utf-8'), packet.address))

            packets_to_delete.append(packet)

        for packet in packets_to_delete:
            self.recv_packets.remove(packet)

    def sendRecievePackets(self):
        inputs = [self.serv_sock]

        readable, _, _ = select.select(
            inputs, [], inputs, 0.01)

        for sock in readable:
            data, client_address = sock.recvfrom(1024)

            try:
                payload = json.loads(data)
                self.recv_packets.append(Packet(payload, client_address))
            except:
                pass

        packets_to_remove = []

        for packet in self.ready_packets:
            self.serv_sock.sendto(packet.payload, packet.address)
            packets_to_remove.append(packet)

        for packet in packets_to_remove:
            self.ready_packets.remove(packet)


serv = Server(('', 5888))
serv.loop()
