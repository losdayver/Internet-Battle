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
        self.sessionPID = 0
        # TODO мб через несколько сокетов
        self.senderQueue = multiprocessing.Manager().Queue()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", self.communicationPort))

    def createSession(self):
        q = multiprocessing.Manager().Queue()
        session = Session(q, self.senderQueue)
        p = multiprocessing.Process(target=session.simulate)
        self.gameSessions[p.pid] = q
        self.sessionPID = p.pid
        p.start()

    def run(self):  # TODO мб select
        self.createSession()

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
        self.gameSessions[self.sessionPID].put([packetDict, addr])

    def sender(self):
        while True:
            try:
                addrs, packet = self.senderQueue.get(False)
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
