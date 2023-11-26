import threading
import queue


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

    def startSimulatingAction(self, packet, meta):  # TODO подумать, отдельный процесс считать изменения и отправлять
        funcDict = self.startSimulatingAction.__dict__

        if meta["uid"] not in funcDict.keys():
            funcDict[meta["uid"]] = {"pressed"}

    def handleCommand(self, command, addr):
        meta = command["meta"]
        for key, value in command.items():
            if key == "connection_data":
                eventType = value["event_type"]
                if eventType == "connect":  # TODO генерить uid тут
                    self.players[meta["uid"]] = Player(meta["uid"], meta["name"], addr)
                elif eventType == "disconnect":
                    del self.players[meta["uid"]]

                connPacket = self.generateConnectionData(meta["uid"], eventType)
                self.sendMessage(self.getAllPlayersAddrs(), connPacket)

            elif key == "input_data":
                self.startSimulatingAction(value, meta)

            elif key == "message_data":  # TODO че с историей сообщений
                msgPacket = self.generateChatData(meta["uid"], value)
                self.sendMessage(self.getAllPlayersAddrs(), msgPacket)
