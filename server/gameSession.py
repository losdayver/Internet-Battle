import string
import threading
import queue
import random
import timeit
import time


class Player:
    def __init__(self, uid, name, addr):
        self.uid = uid
        self.name = name
        self.addr = addr


class Room:  # логика игры
    def __init__(self, session):
        self.pressed = {}
        self.released = {}
        self.map_name = 'map1.json'
        # TODO подумать над организацией отправки пакетов из метода simulate
        self.session: Session = session
        self.dynamic = [{
            "type": "box",
            "id": 1,
            "position": [5, 5],
            "vector": [0, 0]
        }]

    def simulate(self):  # здесь проверяются pressed и released и просчитывается логика
        self.session.sendSceneData(
            self.session.getAllPlayersAddrs(), self.session.generateSceneData(self.dynamic, []))

        print(list(self.pressed.values()))

        if self.pressed:
            if 'left' in list(self.pressed.values())[0]:
                self.dynamic[0]['vector'][0] = -0.1
            elif 'right' in list(self.pressed.values())[0]:
                self.dynamic[0]['vector'][0] = 0.1

        if self.released:
            self.dynamic[0]['vector'][0] = 0

        self.dynamic[0]['position'][0] += self.dynamic[0]['vector'][0]

        self.pressed = {}
        self.released = {}

        print(self.dynamic[0]['position'])

        time.sleep(0.017)

    def addInput(self, pressed, released, uid):
        if pressed:
            self.pressed[uid] = pressed
        if released:
            self.released[uid] = released

    def removePlayer(self, uid):
        pass


class Session:
    def __init__(self, q, sq):
        self.queue = q
        self.sendQueue = sq
        self.players = {}
        self.simFreq = 20  # частота симуляции (кадров в секунду)
        # частота отправки текущего состояния комнаты, (сообщений в секунду)
        self.sendFreq = 20
        self.chatHistory = []
        self.chatLimit = 20
        self.room = Room(self)

    def simulate(self):
        while True:
            self.room.simulate()

            try:
                command, addr = self.queue.get(False)
                try:
                    threading.Thread(target=self.handleCommand,
                                     args=(command, addr)).start()
                except Exception as exc:
                    print(
                        f"Unexpected exception during command processing:\n {exc}")
            except queue.Empty:
                pass

    def generatePlayersData(self):
        pass

    def generateSceneData(self, append: list, remove: list):
        return {
            "type": "scene_data",
            "static": self.room.map_name,
            "dynamic": {
                "append": append,
                "remove": remove
            }
        }

    def generateConnectionData(self, uid, action):
        if action == "connect":
            return {
                "type": "connection",
                "action": "accept",
                "uid": uid
            }
        elif action == "disconnect":
            pass

    def generateChatData(self):
        return {
            "type": "chat_data",
            "messages": self.chatHistory
        }

    def sendSceneData(self, addrs: list, scene_data):
        self.sendQueue.put((addrs, scene_data))

    def sendMessage(self, addrs: list, message):
        self.sendQueue.put((addrs, message))

    def getAllPlayersAddrs(self):
        return [i.addr for i in self.players.values()]

    def addInput(self, uid, pressed, released):
        self.room.addInput(pressed, released, uid)

    def checkAndSend(self):
        start = timeit.default_timer()
        changes = True
        while True:
            # check changes
            if timeit.default_timer() - start >= self.sendFreq:
                start = timeit.default_timer()
                if changes:
                    packet = ""
                    self.sendMessage(self.getAllPlayersAddrs(), packet)

    def handleCommand(self, command, addr):
        packetType = command["type"]

        if packetType == "connection":
            action = command["action"]
            if action == "connect":
                name = command["name"]
                uid = self.genShortUID()
                self.players[uid] = Player(uid, name, addr)
                packet = self.generateConnectionData(uid, action)
                self.sendMessage(self.getAllPlayersAddrs(), packet)
                self.addMessage(
                    "system", f"{self.players[uid].name} connected")
                time.sleep(0.1)  # TODO исправить этот костыль
                self.sendMessage(self.getAllPlayersAddrs(),
                                 self.generateChatData())

            elif action == "disconnect":
                uid = command["uid"]
                self.room.removePlayer(uid)
                del self.players[uid]

        elif packetType == "input":
            uid = command["uid"]
            pressed = command["pressed"]
            released = command["released"]
            self.addInput(uid, pressed, released)

        elif packetType == "message":
            uid = command["uid"]
            text = command["text"]
            self.addMessage(self.players[uid].name, text)
            packet = self.generateChatData()
            self.sendMessage(self.getAllPlayersAddrs(), packet)

    def addMessage(self, name, text):
        self.chatHistory.append({"author": name, "text": text})
        if len(self.chatHistory) > self.chatLimit:
            self.chatHistory = self.chatHistory[len(
                self.chatHistory)-self.chatLimit:]

    def genShortUID(self):
        return "".join([random.choice(string.ascii_letters + string.digits) for _ in range(8)])
