import string
import threading
import queue
import random
import timeit
import time
import json
import os
import math

MAPS_PATH = os.path.join(os.path.dirname(__file__), '..', 'resources', 'maps')
DYNAMIC_INFO = None
with open(os.path.join(os.path.dirname(
        __file__), '..', 'resources', 'misc', 'dynamic_info.json')) as file:
    DYNAMIC_INFO = json.load(file)
SIM_FREQ = 30


# TODO организовать хранение данных сцены в отдельном классе


class Scene:
    def __init__(self):
        self.map_name = 'battleground'

        with open(os.path.join(MAPS_PATH, self.map_name + '.json')) as file:
            j = json.load(file)
            self.static = j['static']
            self.dynamic = j['dynamic']

    def generateSceneUpdatePacket(self):
        return {
            'type': 'scene_data',
            'static': self.map_name,
            'dynamic': {
                'append': self.dynamic,
                'remove': {}
            }
        }

    def generateSceneDiffPacket(self):
        pass

    def processPhysics(self):
        def testEmpty(s):
            for i in s:
                if i != '.':
                    return False

            return True

        def testPlayerIntersect(new_pos):
            intersects = False

            for line in self.static[int(new_pos[1]):int(math.ceil(new_pos[1] + DYNAMIC_INFO['player']['dimensions'][1]))]:
                cells = line[int(math.floor(new_pos[0])):int(
                    math.ceil(new_pos[0] + DYNAMIC_INFO['player']['dimensions'][0]))]

                if not testEmpty(cells):
                    intersects = True
                    break

            return intersects

        toDelete = []

        for d in self.dynamic:
            if d['type'] == 'player':
                d['vector'][1] = min(
                    d['vector'][1] + 0.5 / SIM_FREQ, 20 / SIM_FREQ)

                d['onGround'] = False

                if testPlayerIntersect([d['position'][0], d['position'][1] + d['vector'][1]]):
                    if d['vector'][1] > 0:
                        d['position'][1] = math.ceil(d['position'][1])
                        d['onGround'] = True
                    elif d['vector'][1] < 0:
                        d['position'][1] = int(d['position'][1])

                    d['vector'][1] = 0
                else:
                    d['position'][1] += d['vector'][1]

                if testPlayerIntersect([d['position'][0] + d['vector'][0], d['position'][1]]):
                    if d['vector'][0] > 0:
                        d['position'][0] = math.ceil(d['position'][0])
                    elif d['vector'][0] < 0:
                        d['position'][0] = int(d['position'][0])
                else:
                    d['position'][0] += d['vector'][0]
            else:
                d['position'][0] += d['vector'][0]
                d['position'][1] += d['vector'][1]

            if d['position'][0] > len(self.static[0]) or d['position'][1] > len(self.static) or d['position'][0] < 0 or d['position'][1] < 0:
                toDelete.append(d)

        for d in toDelete:
            self.dynamic.remove(d)

    def processPlayerInput(self, pressed, released):
        for uid in pressed.keys():
            playerDynamic = self.findDynamicPlayer(uid)

            if 'left' in pressed[uid]:
                playerDynamic['vector'][0] = -7 / SIM_FREQ
                playerDynamic['facing'] = 'left'
            if 'right' in pressed[uid]:
                playerDynamic['vector'][0] = 7 / SIM_FREQ
                playerDynamic['facing'] = 'right'
            if 'jump' in pressed[uid] and playerDynamic['onGround']:
                playerDynamic['vector'][1] = -15 / SIM_FREQ

            if 'fire' in pressed[uid]:
                self.addDynamicShotgunBullet(
                    uid, [playerDynamic['position'][0], playerDynamic['position'][1] + 0.5], [25 / SIM_FREQ if playerDynamic['facing'] == 'right' else -25 / SIM_FREQ, 0])

        for uid in released.keys():
            playerDynamic = self.findDynamicPlayer(uid)

            if 'left' in released[uid] and playerDynamic['vector'][0] < 0:
                playerDynamic['vector'][0] = 0
            if 'right' in released[uid] and playerDynamic['vector'][0] > 0:
                playerDynamic['vector'][0] = 0

    def findAvalibleId(self):
        max_id = 0

        for d in self.dynamic:
            max_id = max(d['id'], max_id)

        return max_id + 1

    def addDynamicPlayer(self, uid):
        # TODO Задокументировать какие дополнительные
        # поля могут быть у каких объектов
        # и какие из них нужно отправить клиенту
        self.dynamic.append({
            'type': 'player',
            'id': self.findAvalibleId(),
            'position': [6, 10],
            'vector': [0, 0],
            'uid': uid,
            'facing': 'right',
            'onGround': False,
            'gun': 'shotgun'
        })

    def addDynamicShotgunBullet(self, uid, position, vector):
        # TODO Задокументировать какие дополнительные
        # поля могут быть у каких объектов
        # и какие из них нужно отправить клиенту
        self.dynamic.append({
            'type': 's_bullet',
            'id': self.findAvalibleId(),
            'position': position,
            'vector': vector,
            'uid': uid
        })

    def findDynamicPlayer(self, uid):
        for d in self.dynamic:
            if d['type'] == 'player' and d['uid'] == uid:
                return d


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
        self.chatHistory = []
        self.chatLimit = 20

        self.pressed = {}
        self.released = {}

        self.scene = Scene()

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

            if end_time - start_time < 1/SIM_FREQ:
                time.sleep(1/SIM_FREQ - (end_time - start_time))

    def sceneSimulate(self):
        self.sendSceneData(
            self.getAllPlayersAddrs(), self.scene.generateSceneUpdatePacket())

        self.scene.processPlayerInput(self.pressed, self.released)
        self.scene.processPhysics()

        self.pressed = {}
        self.released = {}

    def generatePlayersData(self):
        pass

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
                self.scene.addDynamicPlayer(uid)

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
