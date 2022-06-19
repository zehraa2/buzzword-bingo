import json
from typing import List
from socket import socket

from modals.Player import Player


# GameModal represents all information about the game (IP, PORT, connection etc.)
# Also has methods for sending messages to client and receiving messages from client


class GameModal(object):
    IP: str
    PORT: int
    FORMAT = "utf-8"
    SIZE = 8192
    connected: bool
    connection: socket
    addr: any
    wordsFile = str
    wordsList = List[str]
    maxPlayers: int
    players: List[Player] = []
    resolution: str = "5x5"

    def __init__(self, IP, PORT, connection, addr, wordsFile, maxPlayers, resolution):
        self.IP = IP
        self.PORT = PORT
        self.ADDR = (IP, PORT)
        self.connection = connection
        self.addr = addr
        self.connected = True
        self.wordsFile = wordsFile
        self.wordsList = self.getWordsFromWordsFile()
        self.maxPlayers = maxPlayers
        self.resolution = int(resolution.split(
            "x")[0]) * int(resolution.split("x")[1])

    @staticmethod
    def jsonToDictionary(jsonStr: str):
        return json.loads(jsonStr)

    @staticmethod
    def dictionaryToJson(dictionary: dict):
        return json.dumps(dictionary, indent=2)

    def getWordsFromWordsFile(self):
        with open(self.wordsFile) as file:
            return file.read().split()

    def sendToClient(self, dictionary: dict):
        encoded = self.dictionaryToJson(dictionary).encode(self.FORMAT)
        self.connection.send(encoded)

    def sendToAll(self, dictionary: dict):
        encoded = self.dictionaryToJson(dictionary).encode(self.FORMAT)
        self.connection.sendall(encoded)

    def receiveMessage(self):
        message = self.connection.recv(self.SIZE).decode(self.FORMAT)
        return self.jsonToDictionary(message)

    def pingClient(self):
        self.sendToClient({"action": "ping"})

    def closeClientConnection(self):
        self.connected = False
        self.connection.close()

    # Player

    def addPlayer(self, player: Player):
        self.players.append(player)

    def getPlayers(self):
        return self.players

    def removePlayer(self, player):
        self.players.remove(player)

    # Setters

    def setWordsList(self, list: List[str]):
        self.wordsList = list

    # Getters

    def getWordsList(self):
        return self.wordsList
