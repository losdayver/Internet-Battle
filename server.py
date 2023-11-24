import socket
import select

if __name__ != '__main__':
    quit()


class Server:
    def __init__(self, address):
        self.address = address
        self.serv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serv_sock.bind(self.address)
        self.serv_sock.setblocking(False)
        self.client_addresses = []

    def loop(self):
        inputs = [self.serv_sock]
        while True:
            readable, writeable, exceptional = select.select(
                inputs, [], inputs, 0.01)

            for sock in readable:
                msg, client_address = sock.recvfrom(1024)
                print(f'Connected by {client_address} with data {msg}')
                if client_address not in self.client_addresses:
                    self.client_addresses.append(client_address)

            # for disconnecting need to implement "ping" packet
            for addr in self.client_addresses:
                self.serv_sock.sendto('bless you'.encode('utf-8'), addr)

            self.client_addresses = []


serv = Server(('', 5888))
serv.loop()
