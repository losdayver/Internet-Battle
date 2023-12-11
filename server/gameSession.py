import string
import threading
import queue
import random
import timeit
import time
import json
import os


class Player:
    def __init__(self, uid, name, addr):
        self.uid = uid
        self.name = name
        self.addr = addr


class Session:
    def __init__(self, q, sq):
        self.queue = q
        self.sendQueue = sq
        self.players = {}
        self.simFreq = 40  # частота симуляции (кадров в секунду)
        self.chatHistory = []
        self.chatLimit = 20

        self.pressed = {}
        self.released = {}
        self.map_name = 'map1.json'

        # TODO Временно решение для заглушки информации о карте
        with open(os.path.join(os.path.dirname(__file__), '..', 'resources', 'maps', self.map_name)) as file:
            j = json.load(file)
            self.static = j['static']
            self.dynamic = j['dynamic']

    def simulate(self):
        while True:
            start_time = time.time()

            try:
                command, addr = self.queue.get(False)

                self.handleCommand(command, addr)
            except queue.Empty:
                pass

            self.sceneSimulate()

            end_time = time.time()

            if end_time - start_time < 1/self.simFreq:
                time.sleep(1/self.simFreq - (end_time - start_time))

    def sceneSimulate(self):
        self.sendSceneData(
            self.getAllPlayersAddrs(), self.generateSceneData(self.dynamic, []))

        uidOnGround = []

        for d in self.dynamic:
            d['position'][0] += d['vector'][0]
            d['position'][1] += d['vector'][1]

            if d['type'] == 'player':
                d['vector'][1] = min(d['vector'][1] + 2 /
                                     self.simFreq, 30 / self.simFreq)

                try:
                    down = self.static[int((d['position'][1] + 65) %
                                           32 + 1)][int(d['position'][0]):int((d['position'][0] + 32) % 32 + 2)]

                    up = self.static[int((d['position'][1]) %
                                         32)][int(d['position'][0]):int((d['position'][0] + 32) % 32 + 2)]

                    print(up)

                    if '#' in up:
                        d['position'][1] = int(d['position'][1] + 1)
                        d['vector'][1] = 0

                    # TODO исправить костыль с #
                    if '#' in down:
                        d['position'][1] = int(d['position'][1])

                        d['vector'][1] = 0

                        uidOnGround.append(d['uid'])

                except:
                    pass

        for uid in self.pressed.keys():
            playerDynamic = self.findDynamicPlayer(uid)

            if 'left' in self.pressed[uid]:
                playerDynamic['vector'][0] = -10 / self.simFreq
            if 'right' in self.pressed[uid]:
                playerDynamic['vector'][0] = 10 / self.simFreq
            if 'jump' in self.pressed[uid] and uid in uidOnGround:
                playerDynamic['vector'][1] = -25 / self.simFreq

        for uid in self.released.keys():
            playerDynamic = self.findDynamicPlayer(uid)

            if 'left' in self.released[uid] and playerDynamic['vector'][0] < 0:
                playerDynamic['vector'][0] = 0
            if 'right' in self.released[uid] and playerDynamic['vector'][0] > 0:
                playerDynamic['vector'][0] = 0

        self.pressed = {}
        self.released = {}

    def generatePlayersData(self):
        pass

    def generateSceneData(self, append: list, remove: list):
        return {
            'type': 'scene_data',
            'static': self.map_name,
            'dynamic': {
                'append': append,
                'remove': remove
            }
        }

    def generateConnectionData(self, uid, action):
        if action == 'connect':
            return {
                'type': 'connection',
                'action': 'accept',
                'uid': uid
            }
        elif action == 'disconnect':
            pass

    def generateChatData(self):
        return {
            'type': 'chat_data',
            'messages': self.chatHistory
        }

    # TODO не вижу смысла оборачивать в функцию
    def sendSceneData(self, addrs: list, scene_data):
        self.sendQueue.put((addrs, scene_data))

    # TODO не вижу смысла оборачивать в функцию
    def sendMessage(self, addrs: list, message):
        self.sendQueue.put((addrs, message))

    def getAllPlayersAddrs(self):
        return [i.addr for i in self.players.values()]

    def addInput(self, uid, pressed, released):
        if pressed:
            self.pressed[uid] = pressed
        if released:
            self.released[uid] = released

    def checkAndSend(self):
        start = timeit.default_timer()
        changes = True
        while True:
            # check changes
            if timeit.default_timer() - start >= self.sendFreq:
                start = timeit.default_timer()
                if changes:
                    packet = ''
                    self.sendMessage(self.getAllPlayersAddrs(), packet)

    def handleCommand(self, command, addr):
        packetType = command['type']

        if packetType == 'connection':
            action = command['action']
            if action == 'connect':
                name = command['name']
                uid = self.genShortUID()
                self.players[uid] = Player(uid, name, addr)
                packet = self.generateConnectionData(uid, action)
                self.sendMessage(self.getAllPlayersAddrs(), packet)
                self.addMessage(
                    'system', f'{self.players[uid].name} connected')
                time.sleep(0.1)  # TODO исправить этот костыль
                self.sendMessage(self.getAllPlayersAddrs(),
                                 self.generateChatData())
                self.addDynamicPlayer(uid)

            elif action == 'disconnect':
                uid = command['uid']
                self.removePlayer(uid)
                del self.players[uid]

        elif packetType == 'input':
            uid = command['uid']
            pressed = command['pressed']
            released = command['released']

            self.addInput(uid, pressed, released)

        elif packetType == 'message':
            uid = command['uid']
            text = command['text']
            self.addMessage(self.players[uid].name, text)
            packet = self.generateChatData()
            self.sendMessage(self.getAllPlayersAddrs(), packet)

    def addMessage(self, name, text):
        self.chatHistory.append({'author': name, 'text': text})
        if len(self.chatHistory) > self.chatLimit:
            self.chatHistory = self.chatHistory[len(
                self.chatHistory)-self.chatLimit:]

    # TODO сделать уникальным
    def genShortUID(self):
        return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(8)])

    def addDynamicPlayer(self, uid):
        max_id = 0

        for d in self.dynamic:
            max_id = max(d['id'], max_id)

        max_id += 1

        self.dynamic.append({
            'type': 'player',
            'id': max_id,
            'position': [6, 14],
            'vector': [0, 0],
            'uid': uid
        })

    def findDynamicPlayer(self, uid):
        for d in self.dynamic:
            if d['type'] == 'player' and d['uid'] == uid:
                return d
