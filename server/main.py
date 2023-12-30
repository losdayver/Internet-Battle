import socket
from gameSession import Session
import multiprocessing
import json
import queue
import threading


class Communicator:
    def __init__(self):
        self.serverIP = socket.gethostbyname(socket.gethostname())
        self.communicationPort = 5888
        self.packetSize = 1024
        self.gameSessions = {}
        self.senderQueue = multiprocessing.Manager().Queue()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", self.communicationPort))

    def createSession(self):
        q = multiprocessing.Manager().Queue()
        playersCount = multiprocessing.Manager().list()
        playersCount.append(0)
        session = Session(q, self.senderQueue, playersCount)
        p = multiprocessing.Process(target=session.simulate)
        p.start()
        self.gameSessions[p.pid] = [q, playersCount, []]
        return p.pid

    def run(self):
        #self.createSession()

        p = multiprocessing.Process(target=self.sender)
        p.start()

        while True:
            try:
                try:
                    content, addr = self.sock.recvfrom(self.packetSize)
                except:
                    continue

                content = content.decode("utf-8")

                self.commandHandler(content, addr)

            except KeyboardInterrupt:
                p.kill()
                return

    def commandHandler(self, content, addr):
        packetDict = json.loads(content)
        if packetDict["type"] == "connection" and packetDict["action"] == "connect":
            sessionFound = False

            for sessionId, data in self.gameSessions.items():
                if data[1][0] < 4:
                    self.gameSessions[sessionId][0].put([packetDict, addr])
                    self.gameSessions[sessionId][2].append(addr)
                    sessionFound = True
                    break

            if not sessionFound:
                newSessionPid = self.createSession()
                self.gameSessions[newSessionPid][0].put([packetDict, addr])
                self.gameSessions[newSessionPid][2].append(addr)
        else:
            for sessionId, data in self.gameSessions.items():
                if addr in data[2]:
                    self.gameSessions[sessionId][0].put([packetDict, addr])
                    break

    def sender(self):
        while True:
            try:
                addrs, packet = self.senderQueue.get(False)
                if "delete" in packet.keys():
                    addr = packet["delete"]
                    for sessionId, data in self.gameSessions.items():
                        if addr in data[2]:
                            self.gameSessions[sessionId][2].remove(addr)
                            break
                    return
                packet = json.dumps(packet)

                for addr in addrs:
                    threading.Thread(target=self.send, args=(
                        packet.encode("utf-8"), addr)).start()

            except queue.Empty:
                pass

    def send(self, message: bytes, addr):
        self.sock.sendto(message, addr)


if __name__ == "__main__":
    Communicator().run()
