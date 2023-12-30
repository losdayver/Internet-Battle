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
SIM_FREQ = 45


# TODO организовать хранение данных сцены в отдельном классе


class Scene:
    def __init__(self):
        self.map_name = 'battleground'
        self.playersCount = 0
        self.winner = None

        with open(os.path.join(MAPS_PATH, self.map_name + '.json')) as file:
            j = json.load(file)
            self.static = j['static']
            self.dynamic = j['dynamic']
            self.spawns = j['spawns']

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

        def testPointIntersecrs(position):
            try:
                return self.static[int(position[1])][int(position[0])] != '.'
            except:
                return False

        toDelete = []

        for d in self.dynamic:
            if d['type'] == 'player':
                d['vector'][1] = min(
                    d['vector'][1] + 0.8 / SIM_FREQ, 30 / SIM_FREQ)

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
            elif d['type'] == 's_bullet':
                center_x = d['position'][0] + \
                    DYNAMIC_INFO['s_bullet']['dimensions'][0] / 2
                center_y = d['position'][1] + \
                    DYNAMIC_INFO['s_bullet']['dimensions'][1] / 2

                if testPointIntersecrs([center_x, center_y]):
                    toDelete.append(d)
                    continue

                for p in self.dynamic:
                    if p['type'] == 'player' and p['uid'] != d['uid'] and not p['dead']:
                        if p['position'][0] < center_x < p['position'][0] + DYNAMIC_INFO['player']['dimensions'][0] and \
                                p['position'][1] < center_y < p['position'][1] + DYNAMIC_INFO['player']['dimensions'][1]:
                            toDelete.append(d)
                            p['dead'] = True
                            continue

                d['position'][0] += d['vector'][0]
                d['position'][1] += d['vector'][1]

            if d['position'][0] > len(self.static[0]) or d['position'][1] > len(self.static) or d['position'][0] < 0 or d['position'][1] < 0:
                toDelete.append(d)

        for d in toDelete:
            self.dynamic.remove(d)

    def processPlayerInput(self, pressed, released):

        for uid in pressed.keys():
            playerDynamic = self.findDynamicPlayer(uid)

            if playerDynamic['dead']:
                continue

            if 'left' in pressed[uid]:
                playerDynamic['vector'][0] = -10 / SIM_FREQ
                playerDynamic['facing'] = 'left'
            if 'right' in pressed[uid]:
                playerDynamic['vector'][0] = 10 / SIM_FREQ
                playerDynamic['facing'] = 'right'
            if 'jump' in pressed[uid] and playerDynamic['onGround']:
                playerDynamic['vector'][1] = -23 / SIM_FREQ

            if 'fire' in pressed[uid]:
                self.addDynamicShotgunBullet(
                    uid, [playerDynamic['position'][0], playerDynamic['position'][1] + 0.9], [32 / SIM_FREQ if playerDynamic['facing'] == 'right' else -32 / SIM_FREQ, 0])

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

    def addDynamicPlayer(self, uid, name, readyToJoin=True):
        self.playersCount += 1
        # TODO Задокументировать какие дополнительные
        # поля могут быть у каких объектов
        # и какие из них нужно отправить клиенту
        self.dynamic.append({
            'type': 'player',
            'id': self.findAvalibleId(),
            'position': self.spawns[self.playersCount-1],
            'vector': [0, 0],
            'uid': uid,
            'facing': 'right',
            'onGround': False,
            'gun': 'shotgun',
            'dead': False if readyToJoin else True,
            'name': name,
        })

    def getAliveCount(self):
        count = 0
        for dObject in self.dynamic:
            if dObject["type"] == "player":
                if not dObject["dead"]:
                    count += 1

        return count

    def removePlayer(self, uid):
        objectToDelete = None
        for dObject in self.dynamic:
            if dObject["type"] == "player":
                if dObject["uid"] == uid:
                    objectToDelete = dObject
                    break

        if objectToDelete:
            self.playersCount -= 1
            self.dynamic.remove(objectToDelete)

    def needToReload(self):
        count = self.getAliveCount()

        if self.playersCount > 1 and count == 1:
            for dObject in self.dynamic:
                if dObject["type"] == "player":
                    if not dObject["dead"]:
                        self.winner = dObject["uid"]

        if self.playersCount > 1 and count in [0, 1]:
            return True

        return False

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

    def deleteDynamicById(self, id):
        dynamicToDelete = None

        for d in self.dynamic:
            if d['id'] == id:
                dynamicToDelete = d

        if dynamicToDelete:
            self.dynamic.remove(dynamicToDelete)


class Player:
    def __init__(self, uid, name, addr):
        self.uid = uid
        self.name = name
        self.addr = addr
        self.score = 0


class Session:
    def __init__(self, q, sq, plCount):
        self.queue = q
        self.sendQueue = sq
        self.players = {}
        self.chatHistory = []
        self.plCount = plCount
        self.chatLimit = 20

        self.pressed = {}
        self.released = {}

        self.scene = Scene()
    # TODO мб разделить частоты симуляции и отправки

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

    # TODO вынести отправку пакетов за пределы симуляции, данный метод будет возвращать только список пакетов на отправку
    def sceneSimulate(self):
        if self.scene.needToReload():
            if self.scene.winner in self.players.keys():
                self.players[self.scene.winner].score += 1

            self.scene = Scene()

            scoresMessage = ""
            for uid, data in self.players.items():
                scoresMessage += f"{data.name}: {data.score}, "
                self.scene.addDynamicPlayer(uid, data.name)

            if scoresMessage:
                self.addMessage("server", scoresMessage)
                packet = self.generateChatData()
                self.sendMessage(self.getAllPlayersAddrs(), packet)

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

    def removePlayer(self, uid):
        toRemove = None

        for u in self.players.keys():
            if u == uid:
                toRemove = u

        if toRemove:
            del self.players[uid]
            self.plCount[0] -= 1

    def handleCommand(self, command, addr):
        packetType = command['type']

        if packetType == 'connection':
            action = command['action']
            if action == 'connect':
                if self.scene.playersCount == 4:
                    self.sendMessage([addr], {"type": "connection", "action": "reject",
                                              "reason": "The room is full!"})
                    return
                name = command['name']
                uid = self.genShortUID()
                self.players[uid] = Player(uid, name, addr)
                self.plCount[0] += 1
                packet = self.generateConnectionData(uid, action)
                self.sendMessage(self.getAllPlayersAddrs(), packet)
                self.addMessage(
                    'server', f'{self.players[uid].name} connected')
                time.sleep(0.1)
                self.sendMessage(self.getAllPlayersAddrs(),
                                 self.generateChatData())
                readyToJoin = True
                if self.scene.getAliveCount() > 1:
                    readyToJoin = False
                self.scene.addDynamicPlayer(uid, name, readyToJoin)

            elif action == 'disconnect':
                uid = command['uid']
                self.addMessage('server', f'{self.players[uid].name} left')
                packet = self.generateChatData()
                self.sendMessage(self.getAllPlayersAddrs(), packet)
                self.removePlayer(uid)
                self.scene.removePlayer(uid)
                self.sendMessage([], {"delete": addr})

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
