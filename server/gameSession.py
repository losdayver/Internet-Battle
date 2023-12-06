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


class Session:
    def __init__(self, q, sq):
        self.queue = q
        self.sendQueue = sq
        self.players = {}
        self.simFreq = 100  # частота симуляции (кадров в секунду)
        self.sendFreq = 10  # частота отправки текущего состояния комнаты, (сообщений в секунду)

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

    def generateConnectionData(self, playerUID, eventType):
        pass

    def generateChatData(self, playerUID, messagePacket):
        pass

    def sendMessage(self, addrs: list, message):
        self.sendQueue.put((addrs, message))

    def getAllPlayersAddrs(self):
        return [i.addr for i in self.players.values()]

    def startSimulatingAction(self, uid, pressed, released):
        funcDict = self.startSimulatingAction.__dict__

        if meta["uid"] not in funcDict.keys():
            funcDict[meta["uid"]] = {"pressed"}

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
            elif action == "disconnect":
                uid = command["uid"]
                del self.players[uid]

        elif packetType == "input":
            uid = command["uid"]
            pressed = command["pressed"]
            released = command["released"]
            self.startSimulatingAction(uid, pressed, released)

    def genShortUID(self):
        return "".join([random.choice(string.ascii_letters + string.digits) for _ in range(8)])
