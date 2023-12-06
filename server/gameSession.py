import string
import threading
import queue
import random
import timeit


class Player:
    def __init__(self, uid, name, addr):
        self.uid = uid
        self.name = name
        self.addr = addr


class Room:  # логика игры
    def __init__(self):
        self.pressed = {}
        self.released = {}

    def simulate(self):  # здесь проверяются pressed и released и просчитывается логика
        pass

    def addInput(self, pressed, released, uid):
        pass

    def removePlayer(self, uid):
        pass


class Session:
    def __init__(self, q, sq):
        self.queue = q
        self.sendQueue = sq
        self.players = {}
        self.simFreq = 100  # частота симуляции (кадров в секунду)
        self.sendFreq = 10  # частота отправки текущего состояния комнаты, (сообщений в секунду)
        self.chatHistory = []
        self.chatLimit = 20
        self.room = Room()

    def simulate(self):
        while True:
            try:
                command, addr = self.queue.get(False)
                try:
                    threading.Thread(target=self.handleCommand, args=(command, addr)).start()
                except Exception as exc:
                    print(f"Unexpected exception during command processing:\n {exc}")
            except queue.Empty:
                pass

    def generatePlayersData(self):
        pass

    def generateRoomData(self):
        pass

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
                self.addMessage("system", f"{self.players[uid].name} connected")
                self.sendMessage(self.getAllPlayersAddrs(), self.generateChatData())

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
            self.chatHistory = self.chatHistory[len(self.chatHistory)-self.chatLimit:]

    def genShortUID(self):
        return "".join([random.choice(string.ascii_letters + string.digits) for _ in range(8)])
