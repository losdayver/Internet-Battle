import socket
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(('127.0.0.1', 5888))

data, address = sock.recvfrom(1024)

print(data, address)

try:
    while True:
        print('1) connection: accept 2) connection: reject 3) room_data')

        inp = int(input())

        if inp == 1:
            sock.sendto(json.dumps(
                {
                    'type': 'connection',
                    'action': 'accept',
                    'uid': '&^%&yughjvGIUy7t6',
                }
            ).encode('utf-8'), address)
        elif inp == 2:
            sock.sendto(json.dumps(
                {
                    'type': 'connection',
                    'action': 'reject',
                    'reason': 'Server rejected your connection request',
                }
            ).encode('utf-8'), address)
        elif inp == 3:
            sock.sendto(json.dumps(
                {
                    'type': 'connection',
                    'action': 'reject',
                    'reason': 'Server rejected your connection request',
                }
            ).encode('utf-8'), address)

except KeyboardInterrupt:
    sock.close()
