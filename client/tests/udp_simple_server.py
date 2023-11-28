import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(('127.0.0.1', 5888))

try:
    while True:
        print(sock.recvfrom(1024))
except KeyboardInterrupt:
    sock.close()
