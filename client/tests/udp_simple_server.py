import socket
import json
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(False)
sock.bind(('127.0.0.1', 5888))

address = None
running = True


def recieve():
    global address

    while running:
        try:
            data, address = sock.recvfrom(1024)
            print(data, address)
        except:
            pass


threading.Thread(target=recieve).start()

try:
    while running:
        print('1) connection: accept')
        print('2) connection: reject')
        print('3) send scene_data1')
        print('4) send scene_data2')
        print('5) send chat_data')

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
                    'type': 'scene_data',
                    'static': {
                        'method': 'file',
                        'file': 'map1.json'
                    },
                    'dynamic': [
                        {
                            'type': 'box1',
                            'id': 1,
                            'position': [5, 5],
                            'vector': [0.0, 0.1]
                        }
                    ]
                }
            ).encode('utf-8'), address)
        elif inp == 4:
            sock.sendto(json.dumps(
                {
                    'type': 'scene_data',
                    'static': {
                        'method': 'file',
                        'file': 'map2.json'
                    },
                    'dynamic': [
                        {
                            'type': 'box1',
                            'id': 1,
                            'position': [5, 5],
                            'vector': [0.0, 0.1]
                        },
                        {
                            'type': 'box1',
                            'id': 2,
                            'position': [10, 5],
                            'vector': [0.1, 0.0]
                        }
                    ]
                }
            ).encode('utf-8'), address)
        elif inp == 5:
            sock.sendto(json.dumps(
                {
                    'type': 'chat_data',
                    'messages': [
                        {'author': 'Vasiya', 'text': 'privet!'},
                        {'author': 'Vitya', 'text': 'zdarova!'},
                        {'author': 'superman', 'text': 'GG'},
                    ]
                }
            ).encode('utf-8'), address)

except KeyboardInterrupt:
    sock.close()
    running = False
